
import os
import sys

try:
    import readline  # This will internally use pyreadline3 (for Windows) if installed 
except ImportError:
    print("[ERROR] readline is not available.")
    sys.exit(1)



# Custom exception for invalid user input
class InvalidUserInputError(Exception):
    """Exception raised when the user input is invalid."""
    def __init__(self, message="Invalid input provided."):
        self.message = message
        super().__init__(self.message)

def main_menu():
    print("\n===== MAIN MENU =====")
    print("1. List Current Files")
    print("2. List Diagrams")
    print("3. Load File")
    print("4. Display Diagram Info")
    print("5. Search")
    print("6. Statistics")
    print("7. Exit")

def search_sub_menu_five():
    print("\n===== SEARCH SUB-MENU =====")
    print("5.1. Find by type")
    print("5.2. Find by dimension")
    print("0. Return to Main Menu")  # Option to go back

def get_valid_user_int(prompt):
    while True:
        user_input = input(prompt).strip()
        try:
            # Attempt to convert the input to an integer
            return int(user_input)
        except ValueError:
            # If conversion fails, raise our custom exception
            try:
                raise InvalidUserInputError("Invalid input. Please enter a valid number.")
            except InvalidUserInputError as e:
                print(e)

def prompt_user_menu() -> int:
    while True:
        main_menu()
        choice = get_valid_user_int("\nEnter an option (1-7): ")

        if choice < 1 or choice > 7:
            print("\nInvalid option. Please select a number between 1 and 7.")
            continue

        return choice

def complete_xml_factory(diagrams_dict=None):
    def completer(text, state):
        if diagrams_dict is not None:
            files = [f for f in diagrams_dict.keys() if f.startswith(text)]
        else:
            files = [f for f in os.listdir() if f.endswith(".xml") and f.startswith(text)]
        return files[state] if state < len(files) else None
    return completer

# Prompt the user for a filename with autocompletion
# If diagrams_dict is not None, it will be used to check if the file is already loaded
# If diagrams_dict is None, it will just return the filename without checking from the directory
def prompt_user_file_name(diagrams_dict=None) -> str:
    readline.set_completer(complete_xml_factory(diagrams_dict))
    readline.parse_and_bind("tab: complete")

    user_input = input("\nEnter the name of the XML file you want to load: ").strip()

    # Optionally disable completer afterward by setting it to None
    readline.set_completer(None)

    return user_input

def prompt_user_exit():
    while(True):
        user_input = input("Are you sure you want to exit? (y/n): ").strip().lower()
        if user_input == 'y':
            return True
        
        elif user_input == 'n':
            return False
        
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def return_current_files()-> list[str]:
    all_files=os.listdir()
    xml_files=[]

    for each_file in all_files:
        if each_file.endswith(".xml"):
            xml_files.append(each_file)

    return xml_files

def list_diagrams(diagrams_dict):
    if len(diagrams_dict) == 0:
        print("No diagrams loaded.")
    else:
        for filename, diagram in diagrams_dict.items():
            print(f"Filename: {filename}")
            print("-" * 20)  # Separator between diagrams


def display_diagram_info(diagrams_dict, file_name):
    """Display formatted information about a specific diagram."""
    diagram = diagrams_dict.get(file_name)
    
    if diagram is None:
        print(f"\n[!] File '{file_name}' is not loaded.\n")
        return

    print("\n" + "=" * 50)
    print(f"📄 Diagram Info for: {file_name}")
    print("=" * 50)

    print(f"📁 Folder:       {diagram.folder}")
    print(f"📂 Path:         {diagram.path}")
    print(f"📝 Filename:     {diagram.filename}")
    print(f"🗃️ Source:       {diagram.source}")
    print(f"📐 Size (W×H×D): {diagram.size}")
    print(f"🔘 Segmented:    {diagram.segmented}")
    print("-" * 50)

    print(f"🧱 Contains {len(diagram.objects)} object(s):")
    for idx, obj in enumerate(diagram.objects, 1):
        print(f"\n   ▶ Object #{idx}")
        print("   " + "-" * 30)
        for attr_name, attr_value in obj.__dict__.items():
            if attr_name == "bndbox":
                attr_value = f"({attr_value[0]}, {attr_value[1]}, {attr_value[2]}, {attr_value[3]})"
                
            print(f"   • {attr_name.capitalize():<12}: {attr_value}")

    print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    # Prompt the user for a choice and display it
    user_choice = prompt_user_menu()
    print("You selected option:", user_choice)
