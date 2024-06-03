import os
import shutil
import zipfile
import platform
import importlib
import subprocess
import sys

if not os.path.exists("servers"):
    os.makedirs("servers")

initial_dir = os.getcwd()

def reset_cd():
    os.chdir(initial_dir)

class ServerManager:
    def __init__(self):
        self.servers_dir = "servers"
        self.backups_dir = "backups"
        self.server_zip_url = "https://alexidians.github.io/SuperDiamondResourcer/server.zip"
        self.temp_dir = "temp"
        self.required_libs = ["requests"]  # Add any additional required libraries here

        # Check and install required libraries
        self.check_install_libs()

    def check_install_libs(self):
        for lib in self.required_libs:
            try:
                importlib.import_module(lib)
            except ImportError:
                print(f"Installing {lib}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

    def list_servers(self):
        servers = os.listdir(self.servers_dir)
        print("Available Servers:")
        for server in servers:
            print(server)

    def launch_server(self, server_name):
        server_dir = os.path.join(self.servers_dir, server_name)
        if platform.system() == "Windows":
            start_script = "start.bat"
            command = f'start {start_script}'
        else:
            start_script = "start.sh"
            command = f'bash {start_script}'

        script_path = os.path.join(server_dir, start_script)
        if os.path.exists(script_path):
            os.chdir(server_dir)
            os.system(command)
        else:
            print("Server start script not found.")

    def update_server(self, server_name):
        update_script_path = os.path.join(self.servers_dir, server_name, "update.py")
        if os.path.exists(update_script_path):
            os.chdir(os.path.join(self.servers_dir, server_name))
            subprocess.check_call([sys.executable, "update.py"])
        else:
            print("Update script not found.")

    def create_backup(self, server_name, backup_name):
        server_path = os.path.join(self.servers_dir, server_name)
        backup_path = os.path.join(self.backups_dir, backup_name)
        shutil.copytree(server_path, backup_path)
        print("Backup created successfully.")

    def restore_backup(self, backup_name, server_name):
        backup_path = os.path.join(self.backups_dir, backup_name)
        server_path = os.path.join(self.servers_dir, server_name)
        shutil.rmtree(server_path)
        shutil.copytree(backup_path, server_path)
        print("Backup restored successfully.")

    def create_server(self, server_name):
        server_path = os.path.join(self.servers_dir, server_name)
        os.makedirs(server_path, exist_ok=True)
        self.download_extract_server(server_name)
        print("Server created successfully.")

    def view_files(self, server_name):
        server_path = os.path.join(self.servers_dir, server_name)
        print(f"Opening files in {server_name} on file explorer")
        os.startfile(server_path)  # Open file explorer to the server directory

    def download_extract_server(self, server_name):
        os.makedirs(self.temp_dir, exist_ok=True)
        zip_file = os.path.join(self.temp_dir, f"{server_name}.zip")
        response = requests.get(self.server_zip_url)
        if response.status_code == 200:
            with open(zip_file, "wb") as f:
                f.write(response.content)
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(os.path.join(self.servers_dir, server_name))
            os.remove(zip_file)
        else:
            print("Failed to download server zip file.")

def main():
    manager = ServerManager()

    while True:
        print("\nOptions:")
        print("1. List Servers")
        print("2. Launch Server")
        print("3. Update Server")
        print("4. Create Backup")
        print("5. Restore Backup")
        print("6. Create Server")
        print("7. View Files")
        print("8. Reload Directories")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            manager.list_servers()
        elif choice == "2":
            server_name = input("Enter server name to launch: ")
            manager.launch_server(server_name)
        elif choice == "3":
            server_name = input("Enter server name to update: ")
            manager.update_server(server_name)
        elif choice == "4":
            server_name = input("Enter server name to backup: ")
            backup_name = input("Enter backup name: ")
            manager.create_backup(server_name, backup_name)
        elif choice == "5":
            backup_name = input("Enter backup name to restore: ")
            server_name = input("Enter server name to restore backup to: ")
            manager.restore_backup(backup_name, server_name)
        elif choice == "6":
            server_name = input("Enter new server name: ")
            manager.create_server(server_name)
        elif choice == "7":
            server_name = input("Enter server name to view files: ")
            manager.view_files(server_name)
        elif choice == "8":
            reset_cd()
            print("Directories reloaded sucesfully")
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
        input("Press enter to continue...")

if __name__ == "__main__":
    main()
