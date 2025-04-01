
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

def get_valid_user_int(prompt,default=None) -> int:
    while True:
        user_input = input(prompt).strip()
        try:
            # Attempt to convert the input to an integer
            return int(user_input)
        except ValueError:
            # If conversion fails, raise our custom exception
            try:
                if user_input == "":
                    if default is not None:
                        return default
                    else:
                        raise InvalidUserInputError("Invalid input. Please enter a valid number.")

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

def prompt_user_bool_option(prompt):
    user_input = input(prompt).strip().lower()
    if user_input in ["yes", "y"]:
        return True
    elif user_input in ["no", "n"]:
        return False
    else:
        # Any other input (including blank) is treated as "all"
        return None

def prompt_user_object_type():
    while True:
        user_input = input("Enter the type of object you want to search for: ").strip()
        if user_input:
            return user_input
        else:
            print("Invalid input. Please enter a valid object type.")

def display_diagrams(data, prompt="Diagrams", error_message="No diagrams found"):
    """Display diagram information from a list or dictionary with a formatted prompt."""
    print("\n" + "=" * 60)
    print(f"{prompt}".center(60))
    print("=" * 60)

    if not data:
        print("\n" + f"[!] {error_message}".center(60)+"\n")
        print("=" * 60 + "\n")
        return
    
    else:
        print()
        if isinstance(data, dict):
            for i, (filename, diagram) in enumerate(data.items(), start=1):
                print(f"  {i:>2}. Filename: {filename}")
                print(f"      Name    : {getattr(diagram, 'filename', 'N/A')}")
                print(f"      Objects : {len(getattr(diagram, 'objects', []))}")
                print("-" * 60)
        elif isinstance(data, list):
            for i, diagram in enumerate(data, start=1):
                print(f"  {i:>2}. {diagram.filename}")
            print()
        else:
            print("[!] Unsupported data type.")

    print("=" * 60 + "\n")

"""
This function displays the information of a specific diagram that is loaded in memory.
It takes a dictionary of diagrams and the filename as input.
It checks if the diagram is loaded, and if so, it prints its details in a formatted manner.
"""
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

def print_error(section_title="Diagrams", error_message="No diagrams loaded in memory"):
    width = 60
    separator = "=" * width
    title = section_title
    error_msg = error_message
    
    print("\n" + separator)
    print(title.center(width))
    print(separator+"\n")
    print(error_msg.center(width) + "\n")
    print(separator + "\n")

def display_statistics(diagrams_dict):
    """Display formatted statistics information by analyzing every diagram."""
    total_width = 60
    separator = "=" * total_width

    nb_loaded_diagrams = 0
    nb_loaded_objects = 0
    diagram_types = set()
    
    min_height = None
    max_height = None
    min_width = None
    max_width = None
    objects_xmin = None
    objects_xmax = None
    objects_ymin = None
    objects_ymax = None

    for diagram in diagrams_dict.values():
        nb_loaded_diagrams += 1
        nb_loaded_objects += diagram.nb_objects  
        diagram_types=diagram_types.union(diagram.obj_types)        

        
        h = diagram.size[1]
        w = diagram.size[0]
        if min_height is None or h < min_height:
            min_height = h
        if max_height is None or h > max_height:
            max_height = h
        if min_width is None or w < min_width:
            min_width = w
        if max_width is None or w > max_width:
            max_width = w

        
        x_min = diagram.xmin
        x_max = diagram.xmax
        y_min = diagram.ymin
        y_max = diagram.ymax
        if objects_xmin is None or x_min < objects_xmin:
            objects_xmin = x_min
        if objects_xmax is None or x_max > objects_xmax:
            objects_xmax = x_max
        if objects_ymin is None or y_min < objects_ymin:
            objects_ymin = y_min
        if objects_ymax is None or y_max > objects_ymax:
            objects_ymax = y_max

    avg_objects = nb_loaded_objects / nb_loaded_diagrams if nb_loaded_diagrams else 0
    diagram_types_str = ", ".join(sorted(diagram_types)) if diagram_types else "None"

    # Print the formatted statistics report
    print("\n" + separator)
    print("Statistics".center(total_width))
    print(separator + "\n")

    print(f"{'Total Diagrams Loaded':<30}: {nb_loaded_diagrams}")
    print(f"{'Total Objects Loaded':<30}: {nb_loaded_objects}")
    print(f"{'Avg Objects per Diagram':<30}: {avg_objects:.2f}")
    print(f"{'Diagram Types':<30}: {diagram_types_str}\n")

    print("Diagram Size (Width x Height):")
    print(f"    {'Min Width':<20}: {min_width}")
    print(f"    {'Max Width':<20}: {max_width}")
    print(f"    {'Min Height':<20}: {min_height}")
    print(f"    {'Max Height':<20}: {max_height}\n")

    print("Object Coordinates:")
    print(f"    {'Xmin':<20}: {objects_xmin}")
    print(f"    {'Xmax':<20}: {objects_xmax}")
    print(f"    {'Ymin':<20}: {objects_ymin}")
    print(f"    {'Ymax':<20}: {objects_ymax}")

    print("\n" + separator + "\n")


if __name__ == "__main__":
    # Prompt the user for a choice and display it
    user_choice = prompt_user_menu()
    print("You selected option:", user_choice)
