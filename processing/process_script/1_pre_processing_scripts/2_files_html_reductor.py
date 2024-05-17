import os
import sys
import re
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

def clean_html_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            contents = file.read()

        soup = BeautifulSoup(contents, 'html.parser')

        # cleanup operations
        # Remove all images
        for img in soup.find_all("img"):
            img.decompose()
        
        # Remove all edit sections
        for edit_section in soup.find_all("span", class_="editsection"):
            edit_section.decompose()
        
        # Remove all span element
        tags_to_remove = ['siteSub', 'column-one', 'footer', 'catlinks']
        for tag_id in tags_to_remove:
            tag = soup.find(id=tag_id)
            if tag:
                tag.decompose()
        
        # Remove all span and following ul
        text_to_remove = ["Note", "Collegamenti esterni", "Voci correlate", "Altri progetti", "Collegamenti"]
        for span in soup.find_all("span", class_="mw-headline"):
            if span.text in text_to_remove:
                parent_h2 = span.find_parent("h2")
                if parent_h2:
                    next_ul = parent_h2.find_next("ul")
                    if next_ul:
                        next_ul.decompose()
                    parent_h2.decompose()

        # Remove index
        if soup.find("table", class_="toc"):
            soup.find("table", class_="toc").decompose()
        
        # Remove references
        if soup.find("div", class_="references-small"):
            soup.find("div", class_="references-small").decompose()

        # Remove NavFrame
        # if soup.find("div", class_="NavFrame"):
        #    soup.find("div", class_="NavFrame").decompose()

        # Define the patterns to find and replace
        patterns = [r'\{\{\{.*?\}\}\}', r'\[\[.*?\]\]']

        # Function to replace unwanted patterns in text
        def replace_patterns(text, patterns):
            for pattern in patterns:
                text = re.sub(pattern, '', text)
            return text
    

        # Iterate through all 'td' elements and replace the patterns
        for td in soup.find_all('td'):
            if any(re.search(pattern, td.text) for pattern in patterns):
                for content in td.contents:
                    if content.string and any(re.search(pattern, content.string) for pattern in patterns):
                        content.replace_with(replace_patterns(content.string, patterns))


        # Remove title
        head_title = soup.find('title')
        if head_title:
            head_title.decompose()

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(str(soup))

    except Exception as e:
        print(f"Failed to process {filepath}: {e}")
        return filepath, False
    return filepath, True

def process_files_concurrently(filepaths):
    results = []
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(clean_html_file, filepath): filepath for filepath in filepaths}
        for future in tqdm(as_completed(futures), total=len(filepaths), desc="Processing HTML Files"):
            filepath, success = future.result()
            if not success:
                print(f"Error processing {filepath}")
            results.append((filepath, success))
    return results

def read_file_paths(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The specified file path does not exist: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as file:
        filepaths = [line.strip() for line in file if line.strip()]
    return filepaths


def main():

    relative_path_to_main = os.path.join(os.pardir, os.pardir)  # Adjust based on actual nesting
    main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path_to_main))
    file_list_path = os.path.join(main_directory, 'files_path_list.txt')

    if not os.path.exists(file_list_path):
        print(f"Error: File not found at {file_list_path}")
        sys.exit(1)

    filepaths = read_file_paths(file_list_path)
    print('\033[33mCLEANING HTML FILES\033[0m\n')
    results = process_files_concurrently(filepaths)
    print("\nFinished cleaning all HTML files.")

if __name__ == "__main__":
    main()

