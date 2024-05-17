import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import spacy
import logging

# basic configuration for logging
logging.basicConfig(filename='lemmatization_errors.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def lemmatize_file(filepath, nlp):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()

        # Process the text with spaCy to lemmatize
        doc = nlp(text)
        lemmatized_text = ' '.join([token.lemma_ for token in doc if not token.is_punct])

        # Write the lemmatized text back to the file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(lemmatized_text)

        return filepath, True
    except Exception as e:
        logging.error(f"Error processing {filepath}: {e}", exc_info=True)
        return filepath, False

def initialize_nlp():
    # Load the Italian NLP model
    return spacy.load('it_core_news_sm', disable=['parser', 'ner'])

def process_files_in_directory(root_dir, nlp):
    filepaths = []
    # Collect all text file paths
    for subdir, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.txt'):  # Adjust if different extension is needed
                filepath = os.path.join(subdir, filename)
                filepaths.append(filepath)

    # Create a pool of processes and process files
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(lemmatize_file, filepath, nlp): filepath for filepath in filepaths}
        results = []

        # Progress bar to monitor processing
        for future in tqdm(as_completed(futures), total=len(filepaths), desc="Lemmatizing files"):
            result = future.result()
            results.append(result)

    # Print results and count any failures
    failures = [result for result in results if not result[1]]
    print(f"Finished processing {len(results) - len(failures)} files. Failures: {len(failures)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <root_directory>")
        sys.exit(1)

    nlp = initialize_nlp()
    root_directory = sys.argv[1]
    print('\033[33mLEMMATIZING TEXT FILES\033[0m\n')
    process_files_in_directory(root_directory, nlp)
