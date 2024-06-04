import subprocess
import sys
import os
import requests
import zipfile
import json
import shutil

# Function to install a module if it's not already installed
def install_module(module_name):
    try:
        __import__(module_name)
    except ImportError:
        print(f"{module_name} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

# Check and install required modules
install_module("requests")

# Define URLs and directories
zip_url = 'https://alexidians.github.io/SuperDiamondResourcer/server.zip'
zip_file = 'server.zip'
extract_dir = 'extracted_files'
config_dir = 'config'
playerdata_dir = 'playerdata'
backups_dir = 'backups'
logs_dir = 'logs'
script_filename = os.path.basename(__file__)

# Download the zip file
response = requests.get(zip_url)
if response.status_code == 200:
    with open(zip_file, 'wb') as file:
        file.write(response.content)
else:
    print('Failed to download zip file')
    input("Press Enter to exit...")
    exit(1)

# Extract the zip file
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Update JSON files in config directory
for root, _, files in os.walk(os.path.join(extract_dir, config_dir)):
    for file in files:
        if file.endswith('.json'):
            new_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(new_file_path, os.path.join(extract_dir, config_dir))
            existing_file_path = os.path.join(config_dir, relative_path)

            if os.path.exists(existing_file_path):
                # Merge existing JSON with new JSON properties
                with open(existing_file_path, 'r') as existing_file:
                    existing_json = json.load(existing_file)
                
                with open(new_file_path, 'r') as new_file:
                    new_json = json.load(new_file)

                merged_json = {**new_json, **existing_json}
                with open(existing_file_path, 'w') as updated_file:
                    json.dump(merged_json, updated_file, indent=4)
            else:
                # Copy new JSON file if it doesn't exist
                os.makedirs(os.path.dirname(existing_file_path), exist_ok=True)
                shutil.copy2(new_file_path, existing_file_path)

# Ensure .ini files exist in config directory
for root, _, files in os.walk(extract_dir):
    for file in files:
        if file.endswith('.ini'):
            new_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(new_file_path, extract_dir)
            existing_file_path = os.path.join(config_dir, relative_path)

            # Check if the .ini file exists, if not, create it
            if not os.path.exists(existing_file_path):
                os.makedirs(os.path.dirname(existing_file_path), exist_ok=True)
                shutil.copy2(new_file_path, existing_file_path)

# Download and overwrite any other files excluding playerdata, backups, config, logs, and script itself
for root, _, files in os.walk(extract_dir):
    for file in files:
        new_file_path = os.path.join(root, file)
        relative_path = os.path.relpath(new_file_path, extract_dir)

        if not relative_path.startswith((playerdata_dir, backups_dir, config_dir, logs_dir)):
            existing_file_path = relative_path
            
            # Ensure existing_file_path is not empty and not the script itself
            if not existing_file_path or existing_file_path == "" or existing_file_path == script_filename:
                continue

            # Check if the directory exists, if not, create it
            dir_name = os.path.dirname(existing_file_path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)

            # Copy new file or overwrite if it exists
            shutil.copy2(new_file_path, existing_file_path)

# Cleanup
os.remove(zip_file)
shutil.rmtree(extract_dir)

print("Update complete.")
input("Press Enter to exit...")
