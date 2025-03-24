from process_file import *
from ui import *
import sys



def main():
    user_choice = prompt_user()  

    if(validate_argv(sys.argv[1])):
        os.chdir(sys.argv[1])
    else:
        no_path_error()
        exit()

    process_user_choice(user_choice)

    while user_choice!=7:
        user_choice=prompt_user()
        process_user_choice(user_choice)
    exit()  

if __name__ == '__main__':
    main()

    
