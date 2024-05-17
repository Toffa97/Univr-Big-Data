import os
import sys
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import time

def should_remove_file(filepath):
    # Check for filename prefixes
    prefixes = ["Discussione~", "Discussioni_template~", "Discussioni_categoria~","Discussioni_aiuto~", "Discussioni_progetto~", "Discussioni_portale~", "Discussioni_immagine~","Discussioni_Wikipedia~","Discussioni_progetto~","Discussioni_utente~", "Immagine~", "Utente~", "Template~", 'Portale~', 'Progetto~', 'Categoria~', 'Aiuto~', 'Wikipedia~', 'File~', 'MediaWiki~', 'Speciale~', 'Modulo~', 'Media~', 'Wikivoyage~', 'WikivoyageDiscussione~', 'WikivoyageUtente~', 'WikivoyageDiscussioni_utente~', 'WikivoyageImmagine~', 'WikivoyageTemplate~', 'WikivoyagePortale~', 'WikivoyageProgetto~', 'WikivoyageCategoria~', 'WikivoyageAiuto~', 'WikivoyageWikipedia~', 'WikivoyageFile~', 'WikivoyageMediaWiki~', 'WikivoyageSpeciale~', 'WikivoyageModulo~', 'WikivoyageMedia~']
    filename = os.path.basename(filepath)
    for prefix in prefixes:
        if filename.startswith(prefix):
            return True
    
    # Check for redirect <p> tag
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            contents = file.read()
        if re.search(r'<p>Redirecting to <a href="[^"]+">[^<]+</a></p>', contents):
            return True
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

    return False

def process_file(filepath):
    if should_remove_file(filepath):
        os.remove(filepath)
        return filepath, True
    return filepath, False

def remove_empty_directories(root_path):
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        if not filenames and not dirnames:  # Check if the directory is empty
            try:
                os.rmdir(dirpath)
                # print(f"Removed empty directory: {dirpath}")
            except OSError as e:
                print(f"Error removing {dirpath}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_files_path_list.txt>")
        sys.exit(1)

    relative_path_to_main = os.path.join(os.pardir, os.pardir)  # Adjust based on actual nesting
    main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path_to_main))
    file_list_path = os.path.join(main_directory, 'files_path_list.txt')
    if not os.path.exists(file_list_path):
        print(f"Error: File list path does not exist: {file_list_path}")
        sys.exit(1)

    with open(file_list_path, 'r', encoding='utf-8') as file:
        filepaths = [line.strip() for line in file if line.strip()]

    results = []
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_file, filepath): filepath for filepath in filepaths}
        for future in tqdm(as_completed(futures), total=len(filepaths), desc="Processing Files"):
            filepath, removed = future.result()
            #if removed:
                #print(f"Removed: {filepath}")
            results.append((filepath, removed))
    
    # Remove empty directories
    print('\033[33mREMOVING UNWANTED FILES AND DIRECTORIES\033[0m\n')
    remove_empty_directories(sys.argv[1])

    print("\nFinished processing all files.")

if __name__ == "__main__":
    main()
