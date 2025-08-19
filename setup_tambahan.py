import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile

def run_cmd(cmd, sudo=False):
    if sudo and shutil.which("sudo"):
        cmd.insert(0, "sudo")
    print(f"[*] Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def file_exists(file_name):
    return shutil.which(file_name) is not None

def main():
    # Deteksi lingkungan (Termux atau Linux biasa)
    if os.path.isdir("/data/data/com.termux/files/usr/bin"):
        bin_dir = "/data/data/com.termux/files/usr/bin"
        print("[*] Detected Termux environment")
    else:
        bin_dir = "/usr/bin"
        print("[*] Detected Linux environment")

    # Cek apakah sudah ada
    if file_exists("zipalign") and file_exists("apksigner"):
        print(f"[✓] zipalign & apksigner sudah terpasang di {bin_dir}")
        sys.exit(0)

    # Install dependensi
    print("[*] Installing dependencies...")
    if shutil.which("pkg"):
        run_cmd(["pkg", "install", "wget", "unzip", "openjdk-17", "-y"])
    elif shutil.which("apt"):
        run_cmd(["apt", "update"], sudo=True)
        run_cmd(["apt", "install", "wget", "unzip", "openjdk-17", "-y"], sudo=True)

    sdk_dir = os.path.expanduser("~/android-sdk")
    os.makedirs(os.path.join(sdk_dir, "cmdline-tools"), exist_ok=True)

    # Download command line tools
    url = "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"
    zip_path = os.path.join(sdk_dir, "cmdline-tools.zip")
    print("[*] Downloading Android SDK Command Line Tools...")
    urllib.request.urlretrieve(url, zip_path)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(os.path.join(sdk_dir, "cmdline-tools"))
    os.rename(os.path.join(sdk_dir, "cmdline-tools", "cmdline-tools"),
              os.path.join(sdk_dir, "cmdline-tools", "latest"))
    os.remove(zip_path)

    # Set PATH sementara
    env = os.environ.copy()
    env["ANDROID_HOME"] = sdk_dir
    env["PATH"] += f":{sdk_dir}/cmdline-tools/latest/bin:{sdk_dir}/platform-tools"

    # Install build-tools
    print("[*] Installing build-tools (zipalign & apksigner)...")
    run_cmd(["yes", "|", "sdkmanager", "build-tools;34.0.0"], sudo=False)

    # Copy hasil ke bin
    src_dir = os.path.join(sdk_dir, "build-tools", "34.0.0")
    for tool in ["zipalign", "apksigner"]:
        src = os.path.join(src_dir, tool)
        dst = os.path.join(bin_dir, tool)
        if os.path.exists(src):
            if bin_dir == "/usr/bin":
                run_cmd(["cp", src, dst], sudo=True)
                run_cmd(["chmod", "+x", dst], sudo=True)
            else:
                shutil.copy(src, dst)
                os.chmod(dst, 0o755)
            print(f"[✓] Installed {tool} → {dst}")
        else:
            print(f"[!] {tool} not found in build-tools")

    print("[✓] Instalasi selesai!")

if __name__ == "__main__":
    main()
