import os
import sys
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import time

def extract_text_from_html(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            contents = file.read()

        # parse HTML content and extract text
        soup = BeautifulSoup(contents, 'html.parser')
        text = soup.get_text(separator=' ')  # Ensure spaces are used to separate text

        # Normalize whitespace and convert text to lowercase
        words = ' '.join(text.split()).lower().split()

        # Write each word to a new line in the file
        with open(filepath, 'w', encoding='utf-8') as file:
            for word in words:
                file.write(word + '\n')  # Explicitly add newline character

    except Exception as e:
        print(f"Failed to process {filepath}: {e}")
        return filepath, False
    return filepath, True

def process_files_for_text_extraction(filepaths):
    # Create a pool of processes
    with ProcessPoolExecutor() as executor:
        # Submit tasks to the executor
        futures = {executor.submit(extract_text_from_html, filepath): filepath for filepath in filepaths}

        # Use tqdm to create a progress bar
        results = []
        for future in tqdm(as_completed(futures), total=len(filepaths), desc="Extracting text from HTML files"):
            result = future.result()
            results.append(result)

        return results

def read_file_paths(file_list_path):
    with open(file_list_path, 'r', encoding='utf-8') as file:
        filepaths = [line.strip() for line in file if line.strip()]
    return filepaths

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_file_list>")
        sys.exit(1)

    relative_path_to_main = os.path.join(os.pardir, os.pardir)  # Adjust based on actual nesting
    main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path_to_main))
    file_list_path = os.path.join(main_directory, 'files_path_list.txt')
    if not os.path.exists(file_list_path):
        print(f"Error: File list path does not exist: {file_list_path}")
        sys.exit(1)

    filepaths = read_file_paths(file_list_path)
    
    print('\033[33mEXTRACTING TEXT FROM HTML FILES\033[0m\n')
    results = process_files_for_text_extraction(filepaths)

    # Print results and count any failures
    failures = [result for result in results if not result[1]]
    print(f"\nFinished extracting text from all HTML files. Failures: {len(failures)}")

