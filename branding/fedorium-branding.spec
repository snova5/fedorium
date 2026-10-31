# COPR account name that publishes Fedorium updates (https://copr.fedorainfracloud.org).
# Change CHANGEME to your COPR username so installed systems get updates.
%global copr_owner CHANGEME
%global copr_project fedorium

Name:           fedorium-branding
Version:        1.8
Release:        1%{?dist}
Summary:        Fedorium Linux branding, wallpapers and the Fedorium Setup profile wizard
License:        MIT AND CC-BY-SA-4.0
URL:            https://copr.fedorainfracloud.org/coprs/%{copr_owner}/%{copr_project}/
BuildArch:      noarch

Source0:        fedorium-logo.svg
Source1:        fedorium-wallpaper-4k.png
Source2:        metadata.json
Source3:        fedorium-setup
Source4:        fedorium-install
Source5:        fedorium-firstlogin
Source6:        fedorium-os-release
Source7:        fedorium-setup.desktop
Source8:        fedorium-setup-autostart.desktop
Source9:        fedorium-firstlogin.desktop
Source10:       kscreenlockerrc
Source11:       sddm-theme.conf.user
Source12:       fedorium.plymouth
Source13:       make-splash.py
Source14:       fedorium-live
Source15:       fedorium-live.service
Source16:       fastfetch-logo.txt
Source17:       fastfetch-config.jsonc
Source18:       anaconda-fedorium.conf
Source19:       kwalletrc
Source20:       fedorium-logo-coding.svg
Source21:       fedorium-wallpaper-coding-4k.png
Source22:       metadata-coding.json
Source23:       fedorium-apply-theme

BuildRequires:  python3
BuildRequires:  python3-pillow
BuildRequires:  aajohan-comfortaa-fonts
BuildRequires:  fontconfig
BuildRequires:  systemd-rpm-macros

Requires:       kdialog
Requires:       konsole
Requires:       pciutils
Requires:       flatpak
Requires:       polkit
Requires:       mokutil
Requires:       plymouth-plugin-two-step
Requires:       plymouth-theme-spinner
Requires:       fastfetch

%description
Fedorium Linux is a Fedora-based KDE Plasma distribution for gaming, coding
and ricing. This package provides its logo, wallpapers, boot splash, fastfetch
logo, installer profile and the Fedorium Setup wizard that installs the
Gaming, Coding and Ricing profiles.

%prep

%build
# boot splash image: logo + "fedorium" in Comfortaa
python3 %{SOURCE13} fedorium-watermark.png

%install
install -Dm644 %{SOURCE0}  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/fedorium-logo.svg
install -Dm644 %{SOURCE0}  %{buildroot}%{_datadir}/pixmaps/fedorium-logo.svg
install -Dm644 %{SOURCE1}  %{buildroot}%{_datadir}/wallpapers/Fedorium/contents/images/3840x2160.png
install -Dm644 %{SOURCE1}  %{buildroot}%{_datadir}/wallpapers/Fedorium/contents/screenshot.png
install -Dm644 %{SOURCE2}  %{buildroot}%{_datadir}/wallpapers/Fedorium/metadata.json
install -Dm755 %{SOURCE3}  %{buildroot}%{_bindir}/fedorium-setup
install -Dm755 %{SOURCE4}  %{buildroot}%{_libexecdir}/fedorium-install
install -Dm755 %{SOURCE5}  %{buildroot}%{_libexecdir}/fedorium-firstlogin
install -Dm755 %{SOURCE6}  %{buildroot}%{_libexecdir}/fedorium-os-release
install -Dm644 %{SOURCE7}  %{buildroot}%{_datadir}/applications/fedorium-setup.desktop
install -Dm644 %{SOURCE8}  %{buildroot}%{_sysconfdir}/xdg/autostart/fedorium-setup.desktop
install -Dm644 %{SOURCE9}  %{buildroot}%{_sysconfdir}/xdg/autostart/fedorium-firstlogin.desktop
install -Dm644 %{SOURCE10} %{buildroot}%{_sysconfdir}/xdg/kscreenlockerrc
install -Dm644 %{SOURCE11} %{buildroot}%{_datadir}/sddm/themes/breeze/theme.conf.user
install -Dm644 %{SOURCE12} %{buildroot}%{_datadir}/plymouth/themes/fedorium/fedorium.plymouth
install -Dm644 fedorium-watermark.png %{buildroot}%{_datadir}/plymouth/themes/fedorium/watermark.png
install -Dm755 %{SOURCE14} %{buildroot}%{_libexecdir}/fedorium-live
install -Dm644 %{SOURCE15} %{buildroot}%{_unitdir}/fedorium-live.service
install -Dm644 %{SOURCE16} %{buildroot}%{_datadir}/fedorium/fastfetch-logo.txt
install -Dm644 %{SOURCE17} %{buildroot}%{_sysconfdir}/xdg/fastfetch/config.jsonc
install -Dm644 %{SOURCE18} %{buildroot}%{_sysconfdir}/anaconda/profile.d/fedorium.conf
install -Dm644 %{SOURCE19} %{buildroot}%{_sysconfdir}/xdg/kwalletrc
install -Dm644 %{SOURCE20} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/fedorium-logo-coding.svg
install -Dm644 %{SOURCE21} %{buildroot}%{_datadir}/wallpapers/FedoriumCoding/contents/images/3840x2160.png
install -Dm644 %{SOURCE21} %{buildroot}%{_datadir}/wallpapers/FedoriumCoding/contents/screenshot.png
install -Dm644 %{SOURCE22} %{buildroot}%{_datadir}/wallpapers/FedoriumCoding/metadata.json
install -Dm755 %{SOURCE23} %{buildroot}%{_libexecdir}/fedorium-apply-theme

%if "%{copr_owner}" != "CHANGEME"
# update repository: installed systems receive new fedorium-branding versions from COPR
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d
cat > %{buildroot}%{_sysconfdir}/yum.repos.d/fedorium.repo <<EOF
[copr:copr.fedorainfracloud.org:%{copr_owner}:%{copr_project}]
name=Fedorium Linux updates
baseurl=https://download.copr.fedorainfracloud.org/results/%{copr_owner}/%{copr_project}/fedora-\$releasever-\$basearch/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://download.copr.fedorainfracloud.org/results/%{copr_owner}/%{copr_project}/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1
EOF
%endif

%post
%{_libexecdir}/fedorium-os-release || :
# spinner and disk-password images come from Fedora's spinner theme
for f in %{_datadir}/plymouth/themes/spinner/*.png; do
    b=$(basename "$f")
    [ "$b" = watermark.png ] || ln -sf "$f" %{_datadir}/plymouth/themes/fedorium/"$b"
done
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
gtk-update-icon-cache -q %{_datadir}/icons/hicolor &>/dev/null || :

%triggerin -- generic-release
%{_libexecdir}/fedorium-os-release || :

%files
%{_datadir}/icons/hicolor/scalable/apps/fedorium-logo.svg
%{_datadir}/icons/hicolor/scalable/apps/fedorium-logo-coding.svg
%{_datadir}/pixmaps/fedorium-logo.svg
%{_datadir}/wallpapers/Fedorium/
%{_datadir}/wallpapers/FedoriumCoding/
%{_datadir}/fedorium/
%{_bindir}/fedorium-setup
%{_libexecdir}/fedorium-install
%{_libexecdir}/fedorium-firstlogin
%{_libexecdir}/fedorium-os-release
%{_libexecdir}/fedorium-live
%{_libexecdir}/fedorium-apply-theme
%{_unitdir}/fedorium-live.service
%{_datadir}/applications/fedorium-setup.desktop
%config(noreplace) %{_sysconfdir}/xdg/autostart/fedorium-setup.desktop
%config(noreplace) %{_sysconfdir}/xdg/autostart/fedorium-firstlogin.desktop
%config(noreplace) %{_sysconfdir}/xdg/kscreenlockerrc
%config(noreplace) %{_sysconfdir}/xdg/kwalletrc
%config(noreplace) %{_sysconfdir}/xdg/fastfetch/config.jsonc
%dir %{_sysconfdir}/anaconda/profile.d
%config(noreplace) %{_sysconfdir}/anaconda/profile.d/fedorium.conf
%{_datadir}/sddm/themes/breeze/theme.conf.user
%dir %{_datadir}/plymouth/themes/fedorium
%{_datadir}/plymouth/themes/fedorium/fedorium.plymouth
%{_datadir}/plymouth/themes/fedorium/watermark.png
%if "%{copr_owner}" != "CHANGEME"
%config(noreplace) %{_sysconfdir}/yum.repos.d/fedorium.repo
%endif

%changelog
* Sat Oct 31 2026 Fedorium Linux - 1.8-1
- Open-source release layout: licenses, COPR update repository
- Boot splash image is now generated during the package build

* Fri Oct 30 2026 Fedorium Linux - 1.7-1
- Fedorium Coding theme (purple logo + wallpaper), applied by the Coding profile

* Fri Oct 30 2026 Fedorium Linux - 1.6-1
- Anaconda profile (efi_dir=fedora) fixes gen_grub_cfgstub on UEFI installs
- os-release ID=fedorium, ID_LIKE=fedora
- KDE Wallet disabled by default

* Fri Oct 30 2026 Fedorium Linux - 1.5-1
- fastfetch: Fedorium ASCII logo and colors as the system default

* Fri Oct 30 2026 Fedorium Linux - 1.4-1
- English (US) UI for Fedorium Setup
- Live session: no password prompt for the installer (polkit rule for liveuser)

* Fri Oct 30 2026 Fedorium Linux - 1.3-1
- fedorium-live: live user and Plasma autologin even if livesys fails

* Fri Oct 30 2026 Fedorium Linux - 1.2-1
- Fedorium boot splash (Plymouth): logo + "fedorium" in Comfortaa on black

* Fri Oct 30 2026 Fedorium Linux - 1.1-1
- Gaming: optional extras (Wine, Winetricks, Prism Launcher, OBS, Bottles,
  CoreCtrl/GreenWithEnvy, emulators)

* Fri Oct 30 2026 Fedorium Linux - 1.0-1
- First release: logo, 4K wallpaper, Fedorium Setup with profiles
