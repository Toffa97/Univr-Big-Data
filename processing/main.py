import os
import sys
import subprocess
import time
from tqdm import tqdm
from utils.counter import count_files_and_size, format_size
from utils.read_filepaths import list_all_files, write_paths_to_file

os.environ["PYTHONUTF8"] = "1"

# script runner
def run_script(script_path, root_path):
    print(f"\nRunning: \033[33m{os.path.basename(script_path)}\033[0m")
    result = subprocess.run([sys.executable, script_path, root_path], capture_output=False, text=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"Error in \033[33m{script_path}\033[0m:")
        print(result.stderr)

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <root_path_for_wikipedia_dump> <mode>")
        sys.exit(1)

    root_path = sys.argv[1]
    mode = sys.argv[2]

    print('\n\nInitializing Processing Procedure\n')
    print(f'Root path for Wikipedia dump: \033[33m{root_path}\033[0m\n')

    # List all files and save to a text file in the same directory as the main script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_list_path = os.path.join(script_dir, "files_path_list.txt")
    file_paths = list_all_files(root_path)
    write_paths_to_file(file_paths, file_list_path)


    # Count files and sizes before processing
    total_files_before, total_size_before = count_files_and_size(root_path)
    print(f"Before processing: \033[33m{total_files_before} files, {format_size(total_size_before)} used\033[0m.\n")

    script_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'process_script')

    # Recursive directory walk
    scripts = []
    for root, dirs, files in os.walk(script_folder):
        for file in files:
            if file.endswith('.py'):
                script_path = os.path.join(root, file)
                if mode == "1" and '1_pre_processing_scripts' in root:
                    scripts.append(script_path)
                elif mode == "2" and '2_active_processing_scripts' in root:
                    scripts.append(script_path)
                elif mode == "0":
                    scripts.append(script_path)

    scripts.sort()

    start_time = time.time()
    progress_bar = tqdm(total=len(scripts), desc="Overall script progress", unit="script")

    for script in scripts:
        run_script(script, root_path)
        progress_bar.update(1)

        # If script starts with '1_', update the file list
        if os.path.basename(script).startswith('1_') or os.path.basename(script).startswith('6_'):
            file_paths = list_all_files(root_path)
            write_paths_to_file(file_paths, file_list_path)

        print('\nEND SCRIPT\n')

    # DEBUG: used to remove useless words inside files.
    #After running all processing scripts, count top words
    #count_top_words_script = os.path.join('utils', 'count_top_words.py')
    #run_script(count_top_words_script, root_path)

    progress_bar.close()
    elapsed_time = time.time() - start_time
    print(f"\nTotal execution time: {elapsed_time:.2f} seconds\n")

    # Count files and sizes after processing
    total_files_after, total_size_after = count_files_and_size(root_path)
    print(f"After processing: {total_files_after} files, {format_size(total_size_after)} used.\n")
    print(f"Difference: {total_files_after - total_files_before} files (from {total_files_before} files), - {format_size((total_size_before - total_size_after))} (from {format_size(total_size_before)})  \n\n.")
    

if __name__ == "__main__":
    main()
