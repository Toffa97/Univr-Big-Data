import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import logging

# Set up basic configuration for logging
logging.basicConfig(filename='deduplication_errors.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def deduplicate_file(filepath):
    """Reads a file, removes duplicated words, and writes the deduplicated text back to the file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()

        # Remove duplicates by turning the text into a set of words and back into a string
        # This simplistic approach does not maintain the original order of words
        words = set(text.split())
        deduplicated_text = ' '.join(words)

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(deduplicated_text)

        return filepath, True
    except Exception as e:
        logging.error(f"Error processing {filepath}: {e}", exc_info=True)
        return filepath, False

def process_files_in_directory(root_dir):
    filepaths = []
    # Collect all text file paths
    for subdir, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.txt'):
                filepath = os.path.join(subdir, filename)
                filepaths.append(filepath)

    # Create a pool of processes and process files
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(deduplicate_file, filepath): filepath for filepath in filepaths}
        results = []

        # Progress bar to monitor processing
        for future in tqdm(as_completed(futures), total=len(filepaths), desc="Deduplicating files"):
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
    print('\033[33mDEDUPLICATING TEXT FILES\033[0m\n')
    process_files_in_directory(root_directory)
