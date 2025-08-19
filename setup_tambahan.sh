#!/bin/bash
# Installer otomatis zipalign & apksigner
# Support Termux & Linux biasa

set -e

# Lokasi target bin
if [ -d "/data/data/com.termux/files/usr/bin" ]; then
    BIN_DIR="/data/data/com.termux/files/usr/bin"
    echo "[*] Detected Termux environment"
else
    BIN_DIR="/usr/bin"
    echo "[*] Detected Linux environment"
fi

# Cek apakah sudah ada
if command -v zipalign >/dev/null 2>&1 && command -v apksigner >/dev/null 2>&1; then
    echo "[✓] zipalign & apksigner sudah terpasang di $BIN_DIR"
    exit 0
fi

# Install dependensi
echo "[*] Installing dependencies..."
if command -v pkg >/dev/null 2>&1; then
    pkg install wget unzip openjdk-17 -y
elif command -v apt >/dev/null 2>&1; then
    sudo apt update
    sudo apt install wget unzip openjdk-17 -y
fi

# Buat folder SDK
SDK_DIR="$HOME/android-sdk"
mkdir -p "$SDK_DIR/cmdline-tools"
cd "$SDK_DIR"

# Download command line tools
echo "[*] Downloading Android SDK Command Line Tools..."
wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O cmdline-tools.zip
unzip -q cmdline-tools.zip -d cmdline-tools
mv cmdline-tools/cmdline-tools cmdline-tools/latest
rm -f cmdline-tools.zip

# Set PATH sementara
export ANDROID_HOME=$SDK_DIR
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools

# Install build-tools
echo "[*] Installing build-tools (zipalign & apksigner)..."
yes | sdkmanager "build-tools;34.0.0" >/dev/null

# Copy ke bin
cp "$SDK_DIR/build-tools/34.0.0/zipalign" "$BIN_DIR/"
cp "$SDK_DIR/build-tools/34.0.0/apksigner" "$BIN_DIR/"
chmod +x "$BIN_DIR/zipalign" "$BIN_DIR/apksigner"

echo "[✓] Instalasi selesai!"
echo "    zipalign path: $BIN_DIR/zipalign"
echo "    apksigner path: $BIN_DIR/apksigner"
