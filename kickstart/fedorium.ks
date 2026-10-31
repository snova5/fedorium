# Fedorium Linux — kickstart pentru ISO live KDE Plasma
# @VER@ și @REPO@ sunt înlocuite automat de build.sh

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

# --- live + instalator ---
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

# --- branding Fedorium (fără mărci Fedora) ---
-fedora-logos*
-fedora-release*
generic-logos
generic-release
generic-release-notes
fedorium-branding

# --- ecran de login ---
sddm
sddm-breeze

# --- ecran de boot ---
plymouth-plugin-two-step
plymouth-theme-spinner

# --- utilitare mereu utile ---
flatpak
pciutils
kdialog
fastfetch
%end

%post --log=/root/fedorium-post.log
set -x
# --- sesiune live KDE (livesys) ---
for u in livesys.service livesys-late.service; do
    systemctl enable "$u" || echo "AVERTISMENT: nu pot activa $u"
done
touch /etc/sysconfig/livesys
if grep -q '^livesys_session=' /etc/sysconfig/livesys; then
    sed -i 's/^livesys_session=.*/livesys_session="kde"/' /etc/sysconfig/livesys
else
    echo 'livesys_session="kde"' >> /etc/sysconfig/livesys
fi

# plasă de siguranță Fedorium: utilizator live + autologin, chiar dacă livesys pică
systemctl enable fedorium-live.service || :

# --- ecranul de login: SDDM ---
systemctl disable plasmalogin.service 2>/dev/null || :
systemctl enable sddm.service || echo "AVERTISMENT: nu pot activa sddm"
systemctl set-default graphical.target

# --- ecranul de boot Fedorium ---
plymouth-set-default-theme fedorium || :

# --- numele sistemului ---
/usr/libexec/fedorium-os-release || :
echo "fedorium" > /etc/hostname

# --- DNS: resolv.conf trebuie să fie link spre systemd-resolved, nu copia de pe PC-ul de build ---
rm -f /etc/resolv.conf
ln -s ../run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
systemctl enable systemd-resolved.service || :

# --- limba: engleză (US) ---
echo 'LANG=en_US.UTF-8' > /etc/locale.conf
printf 'KEYMAP=us\n' > /etc/vconsole.conf

# --- etichete SELinux corecte (build-ul rulează cu SELinux pe permissive) ---
restorecon -RF /etc /usr /var /root /opt 2>/dev/null || :

# rezumat în jurnal
systemctl is-enabled livesys.service livesys-late.service fedorium-live.service sddm.service || :
systemctl get-default || :
%end
