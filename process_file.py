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
    objects=[]

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
    OBJ_NAME_IDX = 0
    POSE_IDX = 1
    TRUNCATED_IDX = 2
    DIFFICULT_IDX = 3
    BNDBOX_IDX = 4
    # Define the attributes of the object   

    BNDBOX=(0, 0, 0, 0) # Placeholder for bounding box coordinates (xmin, ymin, xmax, ymax)


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
        print("\nYou chose: List Current Files")
        choice_one()

    elif choice == 2:
        print("\nYou chose: List Diagrams")
        choice_two(diagrams_dict=diagrams_dict)
        
    elif choice == 3:
        print("\nYou chose: Load File")
        choice_three(diagrams_dict=diagrams_dict)

    elif choice == 4:
        print("\nYou chose: Display Diagram Info")
        choice_four(diagrams_dict=diagrams_dict)
        
    elif choice == 5:
        choice_five(diagrams_dict=diagrams_dict)

    elif choice == 6:
        print("\nYou chose: Statistics")
        choice_six(diagrams_dict=diagrams_dict)
        
    elif choice == 7:
        choice_seven()

    else:
        return
        

def choice_one():
    xml_files=return_current_files()

    try:
        if len(xml_files) == 0:
            raise FolderException("No XML files found in the current directory.")
        
    except FolderException as e:
        print(e)
        return
    
    else:
        for xml_file in xml_files:
            print(xml_file)
        print()

def choice_two(diagrams_dict):

    list_diagrams(diagrams_dict=diagrams_dict)


    

def choice_three(diagrams_dict):
    
    xml_files=return_current_files()

    if(len(xml_files)!=0):
        choice_one()

        file_name=prompt_user_file_name()

        try:
            if is_file_loaded(file_name, diagrams_dict):
                raise FileAlreadyExists(file_name)
            
        except FileAlreadyExists as e:
            print(e)
        
        else:
            try:
                print(f"Loading file: {file_name}")
                if file_name in xml_files:
                    try:
                        load_file(filename=file_name, diagrams_dict=diagrams_dict)
                        
                    except FileNotFoundError:
                        raise FileException("File not found.")

                else:
                    raise FileException(f"File '{file_name}' not found in the current directory.")
            
            except FileException as e:
                print(e)

    else:
        exception=FolderException("No XML files found in the current directory.")
        print(exception)
        

def choice_four(diagrams_dict=None):
    

    if diagrams_dict is None:
        diagrams_dict = {}

    try:
        if len(diagrams_dict) == 0:
            raise DiagramException("No diagrams loaded.")
    
    except DiagramException as e:
        print(e)
        return

    choice_two(diagrams_dict=diagrams_dict)
    file_name=prompt_user_file_name(diagrams_dict=diagrams_dict)

    try:
        display_diagram_info(diagrams_dict=diagrams_dict, file_name=file_name)

    except FileNotFoundError as e:
        print(e)
         

def choice_five(diagrams_dict=None):
    # Enter the sub-menu for Search
    while True:
        search_sub_menu_five()
        sub_choice = input("\nSelect an option (1, 2 or 0): ").strip()

        if sub_choice == "1":
            print("\nYou chose: 5.1. Find by type")
            choice_five_one(diagrams_dict=diagrams_dict)

        elif sub_choice == "2":
            print("\nYou chose: 5.2. Find by dimension")
            # TODO
        elif sub_choice == "0":
            print("Returning to main menu...")
            break
        else:
            print("Invalid search option. Please try again.")
    
def choice_five_one(diagrams_dict=None):
    found_diagrams = search_by_object_type(diagrams_dict=diagrams_dict)

    if len(found_diagrams) == 0:
        print("No objects found with the specified type.")
    else:
        print("Found objects:")
        for diagram in found_diagrams:
            print(diagram.filename)

def choice_six(diagrams_dict=None):
    
    pass

def choice_seven():
    if prompt_user_exit():
        exit()   


def load_file(filename, diagrams_dict=None):
    try:
        with open(filename, 'r') as file:
            xml_data = file.read()

        # Validate XML structure
        try:
            root = ET.fromstring(xml_data)
        except ET.ParseError as parse_error:
            print(f"Error: The file '{filename}' contains invalid XML.\nDetails: {parse_error}")
            return

        folder = root.findtext("folder", default="")
        path = root.findtext("path", default="")
        file_name = root.findtext("filename", default=filename)
        source = root.findtext("source/database", default="Unknown")

        size_elem = root.find("size")
        width = int(size_elem.findtext("width", default="0")) if size_elem is not None else 0
        height = int(size_elem.findtext("height", default="0")) if size_elem is not None else 0
        depth = int(size_elem.findtext("depth", default="0")) if size_elem is not None else 0
        size = (width, height, depth)

        segmented = root.findtext("segmented", default="0") == "1"

        
        objects = []

        for obj_elem in root.findall('object'):
            name = obj_elem.findtext('name', default='')
            pose = obj_elem.findtext('pose', default='Unspecified')
            truncated = int(obj_elem.findtext('truncated', default='0'))
            difficult = int(obj_elem.findtext('difficult', default='0'))

            bndbox = obj_elem.find('bndbox')
            if bndbox is not None:
                xmin = int(bndbox.findtext('xmin', default='0'))
                ymin = int(bndbox.findtext('ymin', default='0'))
                xmax = int(bndbox.findtext('xmax', default='0'))
                ymax = int(bndbox.findtext('ymax', default='0'))
                bbox = [xmin, ymin, xmax, ymax]
            else:
                bbox = [0, 0, 0, 0]

            
            obj = DiagramObject(name, pose, truncated, difficult, bbox)
            objects.append(obj)

        
        diagram = Diagram(
            path=path,
            folder=folder,
            filename=file_name,
            source=source,
            size=size,
            segmented=segmented,
            objects=objects
        )

        
        diagrams_dict[filename] = diagram
        print("File loaded successfully!")

    except FileNotFoundError as e:
        print(f"Error: The file '{filename}' was not found.\nDetails: {e}")
    except ET.ParseError as parse_error:
        print(f"Error: The file '{filename}' contains invalid XML.\nDetails: {parse_error}")
    except Exception as e:
        print(f"An unexpected error occurred while loading the file '{filename}'.\nDetails: {e}")

def is_file_loaded(filename, diagrams_dict=None):
    """Check if a file is already loaded in memory."""
    return filename in diagrams_dict

# Function that searches the loaded diagrams for a specific object type.
# NB: I assumed that the object type is the name of the object in the XML file.
def search_by_object_type(diagrams_dict=None)-> list[Diagram]:
    object_type = prompt_user_object_type()

    if diagrams_dict is None:
        diagrams_dict = {}

    try:
        if len(diagrams_dict) == 0:
            raise DiagramException("No diagrams loaded.")
    except DiagramException as e:
        print(e)
        return  
    
    found_objects = []

    for diagram in diagrams_dict.values():
        for obj in diagram.objects:
            if obj.name == object_type:
                found_objects.append(diagram)
                break

    return found_objects

def search_by_object_dimension():
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
