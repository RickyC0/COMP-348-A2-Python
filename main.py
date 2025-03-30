import os
import sys
import subprocess

from process_file import *
from ui import *


def install_dependencies():
    """Install dependencies listed in dependencies.txt, only once."""
    if os.path.exists(".installed"):
        return

    print("[INFO] Installing project dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "dependencies.txt"])
        with open(".installed", "w") as flag:
            flag.write("installed")
        print("[✓] All dependencies installed successfully.\n")
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to install dependencies.")
        sys.exit(1)


def validate_and_change_directory():
    """Validate the XML folder argument and change to that directory."""
    if len(sys.argv) < 2:
        raise FolderException("Usage: python main.py <folder_path>")
    
    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        raise FolderException(f"[ERROR] The path '{folder_path}' is not a valid directory.")

    os.chdir(folder_path)
    print(f"[✓] Working in directory: {os.getcwd()}")


def main():
    try:
        install_dependencies()

        validate_and_change_directory()

        loaded_objects = {}

        while True:
            user_choice = prompt_user_menu()
            process_user_choice(user_choice, diagrams_dict=loaded_objects)

    except FolderException as e:
        print(e)
    except KeyboardInterrupt:
        print("\n[INFO] Program exited by user.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")


if __name__ == '__main__':
    main()
