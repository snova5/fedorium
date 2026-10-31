<p align="center">
  <img src="branding/files/fedorium-logo.svg" width="160" alt="Fedorium logo">
</p>

<h1 align="center">Fedorium Linux</h1>

<p align="center">A Fedora-based KDE Plasma distribution for <b>gaming</b>, <b>coding</b> and <b>ricing</b>.</p>

---

## Features

- **KDE Plasma** desktop with the KDE apps and **Firefox** preinstalled
- **Fedorium look**: logo on the app launcher, 4K wallpapers (blue *Fedorium* and purple *Fedorium Coding*), boot splash, lock screen and login screen, `fastfetch` with the Fedorium ASCII logo
- **Graphical installer** (Anaconda) that starts from the live desktop with no password prompt
- **Fedorium Setup** opens on first login and installs the profiles you pick:
  - **Gaming** — choose your GPU (AMD / NVIDIA / Intel, auto-detected) for drivers and 32/64-bit Vulkan, plus Steam, Lutris, Heroic, GameMode, MangoHud, Gamescope, ProtonUp-Qt and Discord.
    Optional extras: Wine, Winetricks, Prism Launcher, OBS Studio, Bottles, CoreCtrl / GreenWithEnvy, emulators (RetroArch, PCSX2, Dolphin)
  - **Coding** — GCC, Clang, CMake, Python, Node.js, Rust, Go, Java, Git, Podman, Distrobox, Neovim, VS Code; switches to the purple *Fedorium Coding* theme
  - **Ricing** — Kvantum, Papirus, fastfetch, btop, cava
  - Every profile enables RPM Fusion, Flathub and full multimedia codecs. Run it again anytime from the menu: **Fedorium Setup**.
- English (US) by default; KDE Wallet disabled by default
- Updates for Fedorium's own package through a COPR repository

## Download

Grab the ISO and its `.sha256` file from the [releases page](#) and check it:

```bash
sha256sum -c Fedorium-44-x86_64.iso.sha256
```

Write it to a USB stick with [Ventoy](https://www.ventoy.net/), Fedora Media Writer or `dd`.
On Secure Boot machines with Ventoy, enroll Ventoy's key the first time.

## Build it yourself

You need **Fedora 44** (the build must match the Fedora version it is based on), ~40 GB free disk space and an internet connection. A VM is recommended.

```bash
git clone https://github.com/snova5/fedorium.git
cd fedorium
./build.sh             # Fedora 44 based
# VER=45 ./build.sh    # Fedora 45 based, run on Fedora 45
```

The ISO and its checksum land in `out/`. A build takes 15–60 minutes.
If it fails, check `build/lmc.log` and `/tmp/anaconda.log`.

## Repository layout

```
build.sh                          builds the ISO in one step
kickstart/fedorium.ks             what goes into the ISO
branding/fedorium-branding.spec   the fedorium-branding RPM
branding/files/                   logos, wallpapers, Fedorium Setup, configs
.copr/Makefile                    COPR build recipe for fedorium-branding
docs/PUBLISHING.md                how to publish releases and updates
```

## Troubleshooting

- **Boots to a text console** — pick *Troubleshooting → basic graphics mode* in the boot menu (common with new NVIDIA cards). You can log in as `liveuser` with no password. Logs: `/run/fedorium-live.log`, `/root/fedorium-post.log`.
- **NVIDIA with Secure Boot** — Fedorium Setup asks for a temporary password; on the next reboot choose *Enroll MOK* and type the same password.

## License

Code is [MIT](LICENSE), artwork is [CC BY-SA 4.0](LICENSES.md). The Fedorium name and logo follow the [trademark policy](TRADEMARKS.md).

Fedorium is not affiliated with or endorsed by the Fedora Project or Red Hat.
