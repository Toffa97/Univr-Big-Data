import os
import sys
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import re 
def remove_unwanted_words_from_file(filepath, exact_words_set, punctuated_words_set):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()

        # Handle words attached to punctuation
        # We use a regex pattern that captures any non-whitespace character before and after words in the punctuated_words_set
        for word in punctuated_words_set:
            pattern = rf"\S*{re.escape(word)}\S*"
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        # Now handle exact word matches, ensuring we match whole words only to avoid partial word deletions
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in exact_words_set]

        # Reconstruct the text without unwanted words
        filtered_text = ' '.join(filtered_words)

        # Write the filtered text back to the file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(filtered_text)

        return filepath, True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return filepath, False

def process_files_in_directory(root_dir, exact_words, punctuated_words):
    # Convert lists to sets for faster membership testing
    exact_words_set = set(word.lower() for word in exact_words)
    punctuated_words_set = set(word.lower() for word in punctuated_words)
    filepaths = []

    # Collect all HTML file paths
    for subdir, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.html'):  # Adjust if different extension is needed
                filepath = os.path.join(subdir, filename)
                filepaths.append(filepath)

    # Create a pool of processes and process files
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(remove_unwanted_words_from_file, filepath, exact_words_set, punctuated_words_set): filepath for filepath in filepaths}
        results = []

        # Progress bar to monitor processing
        for future in tqdm(as_completed(futures), total=len(filepaths), desc="Removing specified words"):
            result = future.result()
            results.append(result)

    # Print results and count any failures
    failures = [result for result in results if not result[1]]
    print(f"Finished processing {len(results) - len(failures)} files. Failures: {len(failures)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <root_directory>")
        sys.exit(1)

    root_directory = sys.argv[1]
    exact_words =  ['e','di','da','del','della','delle','dei','degli','dello','dalla','dalle','dallo', 'il', 'la', 'le', 
                      'lo', 'i', 'gli', 'un', 'una', 'uno', 'ma', 'per', 'con', 'in', 'su', 'tra', 'fra', 'sopra', 'sotto', 
                      'sul', 'sotto', 'sugli', 'sulle', 'sulla', 'sulle', 'sullo', 'km', 'm', 'cm', 'mm', 'kg', 'g', 'mg', 
                      'l', 'ml', 'cl', 'dl', 'h', 'min', 'sec', '€', 'km²',' ab.','ab./km²', '|', '·',':', 'che','a','.',',','nel','-','•',
                      '(', ')', '/', 'al', 'non', 'alla', 'alle', 'allo', 'agli', 'ai', 'nei', 'negli', 'nelle', 'nella', 'nelle', 'nello']
    
    punctuated_words = ['(', ')','"']

    print('\033[33mREMOVING UNWANTED WORDS\033[0m\n')
    process_files_in_directory(root_directory, exact_words, punctuated_words)

