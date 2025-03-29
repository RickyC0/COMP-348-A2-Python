from process_file import *
from ui import *
import sys
import os
import subprocess

try:
    import readline
except ImportError:
    import pyreadline3 as readline

def install_dependencies():
    if os.path.exists(".installed"):
        return  # Dependencies already installed

    # Dependency installation logic
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "dependencies.txt"])
        print("All dependencies installed successfully!\n")
        with open(".installed", "w") as f:
            f.write("installed")
    except subprocess.CalledProcessError:
        print("Failed to install dependencies.")
        sys.exit(1)


def main():
    user_choice = prompt_user()  

    if(validate_argv(sys.argv[1])):
        os.chdir(sys.argv[1])
    else:
        no_path_error()
        exit()

    install_dependencies()

    while user_choice!=7:
        user_choice=prompt_user()
        process_user_choice(user_choice)
    exit()  

if __name__ == '__main__':
    main()

    
