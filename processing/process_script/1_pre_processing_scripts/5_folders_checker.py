import os
import sys

def is_directory_empty(dirpath):
    """ Check if a directory is empty or if all its subdirectories are recursively empty """
    try:
        for entry in os.listdir(dirpath):
            full_path = os.path.join(dirpath, entry)
            if os.path.isdir(full_path):
                if not is_directory_empty(full_path):
                    return False
            elif os.path.isfile(full_path):
                return False
        return True
    except OSError as e:
        print(f"Error accessing {dirpath}: {e}")
        return False

def remove_empty_directories(root_path):
    """ Recursively remove directories that are empty or contain only empty subdirectories """
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        if is_directory_empty(dirpath):
            try:
                os.rmdir(dirpath)
                #print(f"Removed empty directory: {dirpath}")
            except OSError as e:
                print(f"Failed to remove {dirpath}: {e}")

                
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_empty_dirs.py <root_directory>")
        sys.exit(1)


    print('\033[33mREMOVE UNWANTED DIRECTORIES AFTER PRE-PROCESSING\033[0m\n')
    print('\n\nNo progress bar here, if it crash you will see.')
    root_directory = sys.argv[1]
    remove_empty_directories(root_directory)

