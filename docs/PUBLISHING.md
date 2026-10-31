# Publishing Fedorium

Three pieces: the source on GitHub, the `fedorium-branding` package on COPR
(so installed systems get updates), and the ISO on SourceForge.

## 1. Source code on GitHub

```bash
cd fedorium
git init -b main
git add .
git commit -m "Fedorium Linux 1.8"
git remote add origin https://github.com/snova5/fedorium.git
git push -u origin main
```

Create the empty repository on github.com first (no README, no license, they
are already here). Then replace `snova5` in `README.md` with your username.

## 2. Update repository on COPR (one-time setup)

1. Create a Fedora account at https://accounts.fedoraproject.org and log in to
   https://copr.fedorainfracloud.org.
2. **New Project**:
   - Name: `fedorium`
   - Chroots: `fedora-44-x86_64` (add `fedora-45-x86_64` when you move to 45)
   - Leave the rest as default, create.
3. In the project: **Packages → New package → SCM**:
   - Package name: `fedorium-branding`
   - Clone URL: `https://github.com/snova5/fedorium.git`
   - Spec file: `branding/fedorium-branding.spec`
   - SRPM build method: **make_srpm**
   - Tick *Auto-rebuild*, save, then **Rebuild**.
4. Optional, for automatic builds on every push: COPR project →
   **Settings → Integrations** shows a GitHub webhook URL; add it under your
   GitHub repo → Settings → Webhooks (content type `application/json`).
5. In `branding/fedorium-branding.spec` change
   `%global copr_owner CHANGEME` to your COPR username, commit and push.
   From now on every Fedorium install gets `/etc/yum.repos.d/fedorium.repo` and
   receives new versions with normal system updates.

## 3. Releasing a new version

1. Make your changes.
2. In the spec: raise `Version:` and add a `%changelog` entry at the top.
3. Commit and push. COPR builds the package (automatically with the webhook,
   otherwise press **Rebuild**). Existing installs update with `sudo dnf upgrade`.
4. Build a new ISO with `./build.sh` when the change matters for new installs.

## 4. ISO downloads

GitHub releases don't accept files over 2 GB, so host the ISO on
SourceForge (free, made for distros) or archive.org.

1. Create a SourceForge project named `fedorium`.
2. Upload `out/Fedorium-44-x86_64.iso` **and** `out/Fedorium-44-x86_64.iso.sha256`.
3. Create a GitHub release with the version and changelog, and link to the
   SourceForge download.

## Before each ISO release, test

- UEFI and legacy BIOS boot; Secure Boot on and off
- Install to disk, reboot, first login → Fedorium Setup
- Each profile on AMD, NVIDIA and Intel if you can
- Internet works in the live session and after install
