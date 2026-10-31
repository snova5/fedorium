#!/bin/bash
# Fedorium Linux — builds the live ISO.
# Run on Fedora (same version as VER), ideally in a VM:  ./build.sh
# Another version:                                      VER=45 ./build.sh
set -euo pipefail

VER="${VER:-44}"
ROOT="$(cd "$(dirname "$0")" && pwd)"
BUILD="$ROOT/build"
OUT="$ROOT/out"

HOSTVER=$(rpm -E %fedora)
if [ "$HOSTVER" != "$VER" ]; then
    echo "WARNING: this system is Fedora $HOSTVER, but you are building Fedorium on Fedora $VER."
    echo "The installer (Anaconda) must match. Run on Fedora $VER, or: VER=$HOSTVER ./build.sh"
    exit 1
fi

echo "==> 1/4 Installing build tools"
sudo dnf -y install lorax lorax-lmc-novirt rpm-build createrepo_c \
    python3-pillow aajohan-comfortaa-fonts fontconfig systemd-rpm-macros

echo "==> 2/4 Building the fedorium-branding package"
sudo rm -rf "$BUILD"
mkdir -p "$BUILD/rpmbuild/SOURCES" "$BUILD/repo"
cp "$ROOT"/branding/files/* "$BUILD/rpmbuild/SOURCES/"
rpmbuild -bb --define "_topdir $BUILD/rpmbuild" "$ROOT/branding/fedorium-branding.spec"
cp "$BUILD"/rpmbuild/RPMS/noarch/*.rpm "$BUILD/repo/"
createrepo_c -q "$BUILD/repo"

echo "==> 3/4 Preparing the kickstart"
sed -e "s|@REPO@|$BUILD/repo|g" -e "s|@VER@|$VER|g" \
    "$ROOT/kickstart/fedorium.ks" > "$BUILD/fedorium-$VER.ks"

echo "==> 4/4 Building the ISO (20–60 min, downloads ~3 GB)"
sudo rm -rf "$OUT"
SEL=$(getenforce)
sudo -v
( while true; do sudo -n true; sleep 50; done ) 2>/dev/null &
KEEPALIVE=$!
[ "$SEL" = "Enforcing" ] && sudo setenforce 0
trap 'if [ "$SEL" = "Enforcing" ]; then sudo setenforce 1; fi; kill $KEEPALIVE 2>/dev/null' EXIT

ISO="Fedorium-$VER-x86_64.iso"
sudo livemedia-creator \
    --ks "$BUILD/fedorium-$VER.ks" \
    --no-virt \
    --make-iso \
    --iso-only \
    --resultdir "$OUT" \
    --project "Fedorium Linux" \
    --volid "Fedorium-$VER" \
    --iso-name "$ISO" \
    --releasever "$VER" \
    --logfile "$BUILD/lmc.log"

sudo chown -R "$(id -u):$(id -g)" "$OUT"
( cd "$OUT" && sha256sum "$ISO" > "$ISO.sha256" )

echo
echo "Done! ISO:      $OUT/$ISO"
echo "      Checksum: $OUT/$ISO.sha256"
