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

def prompt_user() -> int:
    while True:
        main_menu()
        choice = get_valid_user_int("\nEnter an option (1-7): ")

        if choice < 1 or choice > 7:
            print("\nInvalid option. Please select a number between 1 and 7.")
            continue

        return choice

def no_path_error():
    print("You have not specified a folder that could contain XML files to check.")

if __name__ == "__main__":
    # Prompt the user for a choice and display it
    user_choice = prompt_user()
    print("You selected option:", user_choice)
