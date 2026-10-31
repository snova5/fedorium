Name:           fedorium-branding
Version:        1.7
Release:        1%{?dist}
Summary:        Fedorium Linux branding, wallpaper and profile setup wizard
License:        MIT
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
Source13:       fedorium-watermark.png
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
Logo, wallpaper 4K, ecran de blocare și asistentul Fedorium Setup
(profiluri Gaming / Coding / Ricing) pentru Fedorium Linux.

%prep

%build

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
install -Dm644 %{SOURCE13} %{buildroot}%{_datadir}/plymouth/themes/fedorium/watermark.png
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

%post
%{_libexecdir}/fedorium-os-release || :
# spinner-ul și imaginile pentru parola de disc vin din tema spinner a Fedora
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
%{_datadir}/pixmaps/fedorium-logo.svg
%{_datadir}/wallpapers/Fedorium/
%{_bindir}/fedorium-setup
%{_libexecdir}/fedorium-install
%{_libexecdir}/fedorium-firstlogin
%{_libexecdir}/fedorium-os-release
%{_datadir}/applications/fedorium-setup.desktop
%config(noreplace) %{_sysconfdir}/xdg/autostart/fedorium-setup.desktop
%config(noreplace) %{_sysconfdir}/xdg/autostart/fedorium-firstlogin.desktop
%config(noreplace) %{_sysconfdir}/xdg/kscreenlockerrc
%{_datadir}/sddm/themes/breeze/theme.conf.user
%dir %{_datadir}/plymouth/themes/fedorium
%{_datadir}/plymouth/themes/fedorium/fedorium.plymouth
%{_datadir}/plymouth/themes/fedorium/watermark.png
%{_libexecdir}/fedorium-live
%{_unitdir}/fedorium-live.service
%{_datadir}/fedorium/
%config(noreplace) %{_sysconfdir}/xdg/fastfetch/config.jsonc
%dir %{_sysconfdir}/anaconda/profile.d
%config(noreplace) %{_sysconfdir}/anaconda/profile.d/fedorium.conf
%config(noreplace) %{_sysconfdir}/xdg/kwalletrc
%{_datadir}/icons/hicolor/scalable/apps/fedorium-logo-coding.svg
%{_datadir}/wallpapers/FedoriumCoding/
%{_libexecdir}/fedorium-apply-theme

%changelog
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
- fedorium-live: utilizator live + autologin Plasma chiar dacă livesys eșuează

* Fri Oct 30 2026 Fedorium Linux - 1.2-1
- Ecran de boot Fedorium (Plymouth): logo + „fedorium” în Comfortaa, fundal negru

* Fri Oct 30 2026 Fedorium Linux - 1.1-1
- Gaming: extra la alegere (Wine, Winetricks, Prism Launcher, OBS, Bottles,
  CoreCtrl/GreenWithEnvy, emulatoare)

* Fri Oct 30 2026 Fedorium Linux - 1.0-1
- Prima versiune: logo, wallpaper 4K, Fedorium Setup cu profiluri
