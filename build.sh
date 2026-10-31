#!/bin/bash
# Fedorium Linux — construiește ISO-ul
# Rulează pe Fedora (aceeași versiune ca VER), ideal într-un VM: ./build.sh
# Altă versiune: VER=45 ./build.sh
set -euo pipefail

VER="${VER:-44}"
ROOT="$(cd "$(dirname "$0")" && pwd)"
BUILD="$ROOT/build"
OUT="$ROOT/out"

HOSTVER=$(rpm -E %fedora)
if [ "$HOSTVER" != "$VER" ]; then
    echo "ATENȚIE: sistemul tău e Fedora $HOSTVER, dar construiești Fedorium pe baza Fedora $VER."
    echo "Instalatorul (Anaconda) trebuie să fie aceeași versiune. Rulează pe Fedora $VER sau: VER=$HOSTVER ./build.sh"
    exit 1
fi

echo "==> 1/4 Instalez uneltele de build"
sudo dnf -y install lorax lorax-lmc-novirt rpm-build createrepo_c python3-pillow aajohan-comfortaa-fonts fontconfig

echo "==> 2/4 Construiesc pachetul fedorium-branding"
sudo rm -rf "$BUILD"
mkdir -p "$BUILD/rpmbuild/SOURCES" "$BUILD/repo"
cp "$ROOT"/branding/files/* "$BUILD/rpmbuild/SOURCES/"
python3 "$ROOT/branding/make-splash.py" "$BUILD/rpmbuild/SOURCES/fedorium-watermark.png"
rpmbuild -bb --define "_topdir $BUILD/rpmbuild" "$ROOT/branding/fedorium-branding.spec"
cp "$BUILD"/rpmbuild/RPMS/noarch/*.rpm "$BUILD/repo/"
createrepo_c -q "$BUILD/repo"

echo "==> 3/4 Pregătesc kickstart-ul"
sed -e "s|@REPO@|$BUILD/repo|g" -e "s|@VER@|$VER|g" \
    "$ROOT/kickstart/fedorium.ks" > "$BUILD/fedorium-$VER.ks"

echo "==> 4/4 Construiesc ISO-ul (durează 20–60 min, descarcă ~3 GB)"
sudo rm -rf "$OUT"
SEL=$(getenforce)
sudo -v
( while true; do sudo -n true; sleep 50; done ) 2>/dev/null &
KEEPALIVE=$!
[ "$SEL" = "Enforcing" ] && sudo setenforce 0
trap 'if [ "$SEL" = "Enforcing" ]; then sudo setenforce 1; fi; kill $KEEPALIVE 2>/dev/null' EXIT

sudo livemedia-creator \
    --ks "$BUILD/fedorium-$VER.ks" \
    --no-virt \
    --make-iso \
    --iso-only \
    --resultdir "$OUT" \
    --project "Fedorium Linux" \
    --volid "Fedorium-$VER" \
    --iso-name "Fedorium-$VER-x86_64.iso" \
    --releasever "$VER" \
    --logfile "$BUILD/lmc.log"

echo
echo "Gata! ISO-ul e aici: $OUT/Fedorium-$VER-x86_64.iso"
