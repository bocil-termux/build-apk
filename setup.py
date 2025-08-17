import os
import sys
import subprocess
import platform
import time
from threading import Thread
from queue import Queue, Empty

class DependencyInstaller:
    def __init__(self):
        self.is_termux = "com.termux" in os.environ.get("PREFIX", "")
        self.is_linux = platform.system().lower() == "linux"
        self.install_queue = Queue()
        self.loading = False
        self.animation_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        self.animation_index = 0
        self.current_package = ""
        self.success_count = 0
        self.fail_count = 0
        self.skip_count = 0
        self.dependencies = [
            "Pillow", "InquirerPy", "cryptography", "python-dotenv", 
            "requests", "colorama", "rich", "argparse"
        ]
        self.pkg_mapping = {
            "Pillow": None,
            "InquirerPy": None,
            "cryptography": "python-cryptography",
            "python-dotenv": None,
            "requests": "python-requests",
            "colorama": None,
            "rich": None,
            "argparse": None
        }

    def check_required_files(self):
        required_files = ['.data', '.env']
        missing_files = [f for f in required_files if not os.path.exists(f)]
        if missing_files:
            print("\033[1;33mRequired files missing: {}\033[0m".format(", ".join(missing_files)))
            print("\033[1;33mRunning update command...\033[0m")
            if os.path.exists("mulai.py"):
                devnull = open(os.devnull, 'w')
                subprocess.call(
                    ["python3", "mulai.py", "--update"],
                    stdout=devnull,
                    stderr=devnull
                )
                devnull.close()
                print("\033[1;32mUpdate command executed successfully\033[0m")
            else:
                print("\033[1;31mError: mulai.py not found in current directory\033[0m")
            time.sleep(2)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        self.clear_screen()
        print("\033[1;36m" + "=" * 60)
        print(" PYTHON DEPENDENCY INSTALLER".center(60))
        print("=" * 60 + "\033[0m")
        print(f"Detected environment: {'Termux' if self.is_termux else 'Linux'}")
        print(f"Found {len(self.dependencies)} dependencies to install")
        print("\033[1;33m" + "Starting installation..." + "\033[0m")
        print()

    def loading_animation(self):
        while self.loading:
            char = self.animation_chars[self.animation_index % len(self.animation_chars)]
            sys.stdout.write(f"\r\033[1;34m{char}\033[0m Installing \033[1;35m{self.current_package}\033[0m... ")
            sys.stdout.flush()
            self.animation_index += 1
            time.sleep(0.1)

    def run_command(self, command):
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True
            )
            stdout, stderr = process.communicate()
            return process.returncode, stdout, stderr
        except Exception as e:
            return -1, "", str(e)

    def check_installed(self, package):
        try:
            __import__(package.lower().replace("-", "_"))
            return True
        except ImportError:
            return False

    def install_via_pkg(self, package):
        if self.is_termux:
            cmd = f"pkg install -y {package} 2>/dev/null"
        else:
            cmd = f"sudo apt-get install -y {package} 2>/dev/null"
        self.current_package = package
        self.loading = True
        animation_thread = Thread(target=self.loading_animation)
        animation_thread.daemon = True
        animation_thread.start()
        return_code, stdout, stderr = self.run_command(cmd)
        self.loading = False
        animation_thread.join()
        sys.stdout.write("\r" + " " * (len(self.current_package) + 20) + "\r")
        sys.stdout.flush()
        if return_code == 0:
            print(f"\033[1;32m✓\033[0m System package \033[1;35m{package}\033[0m installed successfully")
            return True
        else:
            print(f"\033[1;31m✗\033[0m Failed to install system package \033[1;35m{package}\033[0m")
            return False

    def install_via_pip(self, package):
        self.current_package = package
        self.loading = True
        animation_thread = Thread(target=self.loading_animation)
        animation_thread.daemon = True
        animation_thread.start()
        return_code, stdout, stderr = self.run_command(f"pip install {package} 2>/dev/null")
        self.loading = False
        animation_thread.join()
        sys.stdout.write("\r" + " " * (len(self.current_package) + 20) + "\r")
        sys.stdout.flush()
        if return_code == 0:
            print(f"\033[1;32m✓\033[0m Python package \033[1;35m{package}\033[0m installed successfully")
            return True
        else:
            print(f"\033[1;31m✗\033[0m Failed to install Python package \033[1;35m{package}\033[0m")
            return False

    def install_additional_tools(self):
        print("\033[1;33mInstalling additional tools...\033[0m")
        
        if self.is_termux:
            self.run_command("pkg update -y")
        else:
            self.run_command("sudo apt-get update")

        tools_installation = {
            "keytool": {
                "termux": "pkg install -y openjdk-17",
                "linux": "sudo apt-get install -y openjdk-11-jdk"
            }
        }

        for tool, commands in tools_installation.items():
            self.current_package = tool
            self.loading = True
            animation_thread = Thread(target=self.loading_animation)
            animation_thread.daemon = True
            animation_thread.start()

            cmd = commands["termux"] if self.is_termux else commands["linux"]
            return_code, _, _ = self.run_command(cmd)
            success = return_code == 0

            self.loading = False
            animation_thread.join()
            sys.stdout.write("\r" + " " * (len(self.current_package) + 20) + "\r")
            sys.stdout.flush()

            if success:
                print(f"\033[1;32m✓\033[0m Tool \033[1;35m{tool}\033[0m installed successfully")
                self.success_count += 1
            else:
                print(f"\033[1;31m✗\033[0m Failed to install tool \033[1;35m{tool}\033[0m")
                self.fail_count += 1

    def install_dependencies(self):
        self.check_required_files()
        self.print_header()
        
        for dep in self.dependencies:
            if self.check_installed(dep):
                print(f"\033[1;33m→\033[0m \033[1;35m{dep}\033[0m is already installed")
                self.skip_count += 1
                continue
            
            pkg_name = self.pkg_mapping.get(dep)
            success = False
            
            if pkg_name:
                success = self.install_via_pkg(pkg_name)
                if success:
                    self.success_count += 1
                    continue
            
            if self.install_via_pip(dep):
                self.success_count += 1
            else:
                self.fail_count += 1
        
        self.install_additional_tools()
        
        print("\n\033[1;36m" + "=" * 60)
        print(" INSTALLATION SUMMARY ".center(60))
        print("=" * 60 + "\033[0m")
        print(f"\033[1;32mSuccessfully installed: {self.success_count}\033[0m")
        print(f"\033[1;33mSkipped (already installed): {self.skip_count}\033[0m")
        print(f"\033[1;31mFailed to install: {self.fail_count}\033[0m")
        print("\033[1;36m" + "=" * 60 + "\033[0m")
        
        if self.fail_count > 0:
            print("\n\033[1;31mSome dependencies failed to install. You may need to install them manually.\033[0m")
        
        print("\nInstallation complete!")

if __name__ == "__main__":
    try:
        installer = DependencyInstaller()
        installer.install_dependencies()
    except KeyboardInterrupt:
        print("\n\033[1;31mInstallation cancelled by user.\033[0m")
        sys.exit(1)
