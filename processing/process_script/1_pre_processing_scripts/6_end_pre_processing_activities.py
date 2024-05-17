import os
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

def html_to_text(html_file_path, text_file_path):
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text(separator='\n')
        with open(text_file_path, 'w', encoding='utf-8') as file:
            file.write(text_content)
        # After successful conversion, remove the HTML file
        os.remove(html_file_path)
    except Exception as e:
        print(f"Error processing {html_file_path}: {str(e)}")
        return html_file_path, False
    return html_file_path, True

def process_files_concurrently(filepaths):
    results = []
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(html_to_text, filepath, filepath.replace('.html', '.txt')): filepath for filepath in filepaths if filepath.endswith('.html')}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Converting HTML to TXT"):
            filepath, success = future.result()
            if not success:
                print(f"Error processing {filepath}")
            results.append((filepath, success))
    return results

def process_directory(root_directory):
    filepaths = []
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.html'):
                filepaths.append(os.path.join(root, file))
    return filepaths

def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <root_directory>")
        sys.exit(1)

    print('\033[33mPRE-PROCESSING AND CONVERSION FROM HTML TO TXT STARTED\033[0m\n')
    root_directory = sys.argv[1]
    filepaths = process_directory(root_directory)
    results = process_files_concurrently(filepaths)
    print("\nFinished pre-processing and conversion.\n\n")

if __name__ == "__main__":
    main()
