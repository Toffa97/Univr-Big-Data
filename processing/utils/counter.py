import os
import sys

def count_files_and_size(root_dir):
    total_files = 0
    total_size = 0  # In bytes

    # Traverse directories and files
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            total_files += 1
            total_size += os.path.getsize(file_path)

    return total_files, total_size

def format_size(bytes, suffix='B'):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <root_directory>")
        sys.exit(1)

    root_directory = sys.argv[1]
    total_files, total_size = count_files_and_size(root_directory)
    print(f"Files: {total_files}, Size: {format_size(total_size)}")
