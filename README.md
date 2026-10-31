# Fedorium Linux

Distro bazat pe Fedora, cu KDE Plasma, pentru gaming, coding și ricing.

## Ce conține

- **KDE Plasma** complet + aplicațiile KDE + **Firefox** preinstalat
- **Branding Fedorium**: logo-ul SVG (inclusiv pe butonul de meniu), wallpaper 4K pe desktop, pe ecranul de blocare și la login, numele „Fedorium Linux” în sistem. Mărcile Fedora sunt scoase (`generic-logos`).
- **Fedorium Setup**: pornește singur la prima logare după instalare și te lasă să alegi profilurile:
  - **Gaming**: alegi placa video (AMD / NVIDIA / Intel, detectată automat) → drivere + Vulkan 32/64 biți, Steam, Lutris, GameMode, MangoHud, Gamescope, Heroic, ProtonUp-Qt, Discord
    - Extra la alegere (bifezi): Wine, Winetricks, Prism Launcher, OBS Studio, Bottles, CoreCtrl (AMD) / GreenWithEnvy (NVIDIA), emulatoare (RetroArch, PCSX2, Dolphin)
  - **Coding**: GCC, Clang, CMake, Python, Node.js, Rust, Go, Java, Git, Podman, Distrobox, Neovim, VS Code
  - **Ricing**: Kvantum, Papirus, fastfetch, btop, cava
  - Activează automat RPM Fusion, Flathub și codec-urile complete.
  - Îl poți rula oricând din meniu: **Fedorium Setup**.

## Structura

```
build.sh                          construiește ISO-ul (un singur pas)
kickstart/fedorium.ks             ce intră în ISO
branding/fedorium-branding.spec   pachetul RPM cu branding + Setup
branding/files/                   logo, wallpaper, scripturile Setup
```

## Cum construiești ISO-ul

Recomandat: într-un **VM cu Fedora 44 KDE** (min. 4 GB RAM, 40 GB disc), ca să nu atingi sistemul principal.
Versiunea Fedora din VM trebuie să fie aceeași cu cea pe care o construiești.

```bash
cd fedorium
chmod +x build.sh
./build.sh            # Fedora 44
# VER=45 ./build.sh   # după ce iese Fedora 45, rulat pe Fedora 45
```

ISO-ul apare în `out/Fedorium-44-x86_64.iso`. Dacă ceva eșuează, uită-te în `build/lmc.log` și în `/tmp/*.log` (anaconda) și trimite-mi eroarea.

## Testare

În VirtualBox: VM nou, tip Linux / Fedora 64-bit, 4 GB RAM, 30 GB disc, **EFI activat**, atașezi ISO-ul.
Sesiunea live pornește în KDE → „Install to Hard Drive” → după reboot și logare apare Fedorium Setup.

## Dacă nu pornește în KDE

- În meniul ISO-ului încearcă **Troubleshooting → basic graphics mode** (util la plăci NVIDIA noi).
- În tty te poți loga cu `liveuser`, fără parolă.
- Trimite conținutul acestor fișiere: `/run/fedorium-live.log` și `/root/fedorium-post.log` (cu `sudo cat`).

## Note

- **NVIDIA + Secure Boot**: Setup-ul îți cere o parolă temporară; la primul reboot alegi *Enroll MOK* și introduci aceeași parolă.
- Profilurile se instalează de pe internet după instalare, ca ISO-ul să rămână mic și pachetele să fie la zi.
