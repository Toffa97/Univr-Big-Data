
"""
__all__ = ["get_filepaths"]

def get_filepaths(filename: str):
    filepaths: list[str] = []
    
    with open(filename, "r") as file:
        for line in file:
            filepaths.append(line.strip())

    return filepaths

from ../utils.read_filepaths import get_filepaths

filepaths = get_filepaths(nomefile)

...

"""
import os

def list_all_files(root_directory):
    """Lists all files in the directory and subdirectories."""
    file_paths = []
    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            filepath = os.path.join(subdir, file)
            file_paths.append(filepath)
    return file_paths

def write_paths_to_file(file_paths, file_path):
    """Writes a list of file paths to a text file using UTF-8 encoding."""
    with open(file_path, 'w', encoding='utf-8') as file:
        for path in file_paths:
            file.write(path + "\n")
