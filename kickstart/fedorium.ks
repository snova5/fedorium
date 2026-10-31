# Fedorium Linux — kickstart for the KDE Plasma live ISO
# @VER@ and @REPO@ are filled in by build.sh

lang en_US.UTF-8
keyboard --vckeymap=us --xlayouts='us'
timezone Europe/Bucharest
selinux --enforcing
firewall --enabled --service=mdns
network --bootproto=dhcp --device=link --activate
rootpw --lock
services --enabled=NetworkManager,ModemManager --disabled=sshd
bootloader --location=none
zerombr
clearpart --all
part / --size 14336 --fstype ext4
shutdown

url --mirrorlist=https://mirrors.fedoraproject.org/mirrorlist?repo=fedora-@VER@&arch=x86_64
repo --name=updates --mirrorlist=https://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-f@VER@&arch=x86_64
repo --name=fedorium --baseurl=file://@REPO@

%packages
# --- desktop KDE Plasma ---
@^kde-desktop-environment
@kde-apps
@kde-media
firefox

# --- live session + installer ---
anaconda-live
@anaconda-tools
dracut-live
dracut-config-generic
-dracut-config-rescue
livesys-scripts
glibc-all-langpacks
langpacks-en
kernel
kernel-modules
kernel-modules-extra

# --- boot ISO (BIOS + UEFI) ---
grub2-efi-x64
grub2-efi-x64-cdboot
grub2-pc
grub2-pc-modules
shim-x64
efibootmgr

# --- Fedorium branding (no Fedora trademarks) ---
-fedora-logos*
-fedora-release*
generic-logos
generic-release
generic-release-notes
fedorium-branding

# --- login screen ---
sddm
sddm-breeze

# --- boot splash ---
plymouth-plugin-two-step
plymouth-theme-spinner

# --- always-useful tools ---
flatpak
pciutils
kdialog
fastfetch
%end

%post --log=/root/fedorium-post.log
set -x
# --- KDE live session (livesys) ---
for u in livesys.service livesys-late.service; do
    systemctl enable "$u" || echo "WARNING: cannot enable $u"
done
touch /etc/sysconfig/livesys
if grep -q '^livesys_session=' /etc/sysconfig/livesys; then
    sed -i 's/^livesys_session=.*/livesys_session="kde"/' /etc/sysconfig/livesys
else
    echo 'livesys_session="kde"' >> /etc/sysconfig/livesys
fi

# Fedorium safety net: live user + autologin even if livesys fails
systemctl enable fedorium-live.service || :

# --- login screen: SDDM ---
systemctl disable plasmalogin.service 2>/dev/null || :
systemctl enable sddm.service || echo "WARNING: cannot enable sddm"
systemctl set-default graphical.target

# --- Fedorium boot splash ---
plymouth-set-default-theme fedorium || :

# --- system name ---
/usr/libexec/fedorium-os-release || :
echo "fedorium" > /etc/hostname

# --- DNS: resolv.conf must link to systemd-resolved, not be a copy from the build host ---
rm -f /etc/resolv.conf
ln -s ../run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
systemctl enable systemd-resolved.service || :

# --- language: English (US) ---
echo 'LANG=en_US.UTF-8' > /etc/locale.conf
printf 'KEYMAP=us\n' > /etc/vconsole.conf

# --- fix SELinux labels (the build runs with SELinux permissive) ---
restorecon -RF /etc /usr /var /root /opt 2>/dev/null || :

# summary in the log
systemctl is-enabled livesys.service livesys-late.service fedorium-live.service sddm.service || :
systemctl get-default || :
%end
