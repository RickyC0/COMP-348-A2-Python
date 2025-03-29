from ui import *
import os
import sys
import xml.etree.ElementTree as ET


class FolderException(Exception):
    def __init__(self, message="You have not specified a folder that could contain XML files to check."):
        self.message = message
        super().__init__(self.message)


class FileException(FolderException):
    def __init__(self, message="File not Found Error."):
        self.message = message
        super().__init__(self.message)

class FileAlreadyExists(FileException):
    def __init__(self, filename, message=None):
        if message is None:
            message = f"The file {filename} is already loaded in memory."
        self.message = message
        super().__init__(self.message)

class DiagramException(Exception):
    def __init__(self, message="An error occurred while processing the diagram."):
        self.message = message
        super().__init__(self.message)

class DiagramObjectException(Exception):
    def __init__(self, message="An error occurred while processing the diagram object."):
        self.message = message
        super().__init__(self.message)



class Diagram:
    def __init__(self, path: str, folder: str, filename: str, source: str, size: tuple, segmented: bool, objects: list = None):
        """
        Represents an XML file diagram.
        
        :param path: Path to the file.
        :param folder: Folder where the file is located.
        :param filename: Name of the file.
        :param source: Source information.
        :param size: Tuple representing the dimensions (e.g., (width, height)).
        :param segmented: Boolean indicating if the diagram is segmented.
        :param objects: List of DiagramObject instances (defaults to an empty list).
        """
        self.path = path
        self.folder = folder
        self.filename = filename
        self.source = source
        self.size = size
        self.segmented = segmented
        self.objects = objects if objects is not None else []

    def __str__(self) -> str:
        # Create a multi-line string representation of the diagram
        objects_str = "\n".join(str(obj) for obj in self.objects)
        return (
            f"Path: {self.path}\n"
            f"Folder: {self.folder}\n"
            f"Filename: {self.filename}\n"
            f"Source: {self.source}\n"
            f"Size: {self.size}\n"
            f"Segmented: {self.segmented}\n"
            f"Objects:\n{objects_str}\n"
        )

    def __repr__(self) -> str:
        return (f"Diagram(path={self.path!r}, folder={self.folder!r}, "
                f"filename={self.filename!r}, source={self.source!r}, "
                f"size={self.size!r}, segmented={self.segmented!r}, objects={self.objects!r})")

    def add_object(self, diagram_object: 'DiagramObject'):
        """Adds a DiagramObject to the objects list."""
        self.objects.append(diagram_object)


class DiagramObject:
    def __init__(self, name: str, pose: str, truncated: bool, difficult: bool, bndbox: tuple):
        """
        Represents an object within a diagram.
        
        :param name: Name of the object.
        :param pose: Pose information.
        :param truncated: Boolean indicating if the object is truncated.
        :param difficult: Boolean indicating if the object is difficult.
        :param bndbox: Tuple representing bounding box (e.g., (xmin, ymin, xmax, ymax)).
        """
        self.name = name
        self.pose = pose
        self.truncated = truncated
        self.difficult = difficult
        self.bndbox = bndbox

    def __str__(self) -> str:
        return (
            f"Name: {self.name}\n"
            f"Pose: {self.pose}\n"
            f"Truncated: {self.truncated}\n"
            f"Difficult: {self.difficult}\n"
            f"Bndbox: {self.bndbox}\n"
        )

    def __repr__(self) -> str:
        return (f"DiagramObject(name={self.name!r}, pose={self.pose!r}, "
                f"truncated={self.truncated!r}, difficult={self.difficult!r}, "
                f"bndbox={self.bndbox!r})")


# Function that executes the appropriate logic based on what the user selected
def process_user_choice(choice,diagrams_dict=None):
    if diagrams_dict is None:
        diagrams_dict = {}
    if choice == 1:
            choice_one()

    elif choice == 2:
        choice_two(diagrams_dict=diagrams_dict)
        
    elif choice == 3:
        choice_three(diagrams_dict=diagrams_dict)

    elif choice == 4:
        choice_four()
        
    elif choice == 5:
        choice_five()

    elif choice == 6:
        choice_six()
        
    elif choice == 7:
        choice_seven()

    else:
        return
        

def choice_one():
    print("\nYou chose: List Current Files")
    xml_files=list_current_files()

    if len(xml_files)==0:
        print("No XML files found in the current directory.")
    else:
        for xml_file in xml_files:
            print(xml_file)
        print()

def choice_two(diagrams_dict):
    print("\nYou chose: List Diagrams")

    list_diagrams(diagrams_dict=diagrams_dict)
        # Enter the sub-menu for Search
        while True:
            search_sub_menu_five()
            sub_choice = input("\nSelect an option (1, 2 or 0): ").strip()

            if sub_choice == "1":
                print("\nYou chose: 5.1. Find by type")
                # TODO
            elif sub_choice == "2":
                print("\nYou chose: 5.2. Find by dimension")
                # TODO
            elif sub_choice == "0":
                print("Returning to main menu...")
                break
            else:
                print("Invalid search option. Please try again.")
    elif choice == 6:
        print("\nYou chose: Statistics")
        # TODO
    elif choice == 7:
        exit()

    else:
        return
        

def list_current_files():
    all_files=os.listdir()
    xml_files=[]

    for each_file in all_files:
        if(each_file.__contains__(".xml")):
            xml_files.append(each_file)

    for xml_file in xml_files:
        print(xml_file)
    


def list_diagrams():
    return None

def load_file():
    return None

def display_diagram_info():
    return None

def search_by_type():
    return None

def search_by_dimension():
    return None

def show_statistics():
    return None

def validate_argv(path):
    if not isinstance(path,str):
        return False

    elif not os.path.exists(path):
        return False
    
    elif not os.path.isdir(path):
        return False
    
    else:
        return True


def exit():
    print("\nThe system will exit. Goodbye!")
    sys.exit(1)


if __name__=="__main__":
    choice=prompt_user_menu()
    
    process_user_choice(choice)
    while choice!=7:
        choice=prompt_user_menu()
        process_user_choice(choice)
    exit()
