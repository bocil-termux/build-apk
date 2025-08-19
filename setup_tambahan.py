#!/data/data/com.termux/files/usr/bin/bash

# ========================================
# Setup Android SDK di Termux
# ========================================

set -e

ANDROID_DIR=$HOME/Android
SDK_DIR=$ANDROID_DIR/sdk
CMDLINE_DIR=$ANDROID_DIR/cmdline-tools
BUILD_TOOLS_VERSION=34.0.0

echo "[*] Update pkg..."
pkg update -y && pkg upgrade -y

echo "[*] Install Java..."
pkg install openjdk-17 wget unzip -y

echo "[*] Membuat folder Android SDK..."
mkdir -p $CMDLINE_DIR
mkdir -p $SDK_DIR

echo "[*] Download Command-line Tools..."
cd $CMDLINE_DIR
wget -q https://dl.google.com/android/repository/commandlinetools-linux-10406996_latest.zip -O cmdtools.zip
unzip -q cmdtools.zip
rm cmdtools.zip
mv cmdline-tools latest

# Update PATH sementara untuk script ini
export ANDROID_HOME=$SDK_DIR
export PATH=$PATH:$CMDLINE_DIR/latest/bin
export PATH=$PATH:$SDK_DIR/build-tools/$BUILD_TOOLS_VERSION

echo "[*] Install Build-tools (zipalign + apksigner)..."
yes | sdkmanager --sdk_root=$ANDROID_HOME "build-tools;$BUILD_TOOLS_VERSION"

echo "[*] Tambahkan PATH ke ~/.bashrc..."
if ! grep -q "ANDROID_HOME" ~/.bashrc; then
    echo "export ANDROID_HOME=$SDK_DIR" >> ~/.bashrc
    echo "export PATH=\$PATH:$CMDLINE_DIR/latest/bin" >> ~/.bashrc
    echo "export PATH=\$PATH:\$ANDROID_HOME/build-tools/$BUILD_TOOLS_VERSION" >> ~/.bashrc
fi

echo "[+] Instalasi selesai!"
echo "    Jalankan: source ~/.bashrc"
echo "    Tes: zipalign -h  dan  apksigner --version"
