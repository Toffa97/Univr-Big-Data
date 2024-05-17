# count_top_words.py

import os
import sys
from collections import Counter

def count_words_in_files(root_dir):
    word_count = Counter()

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):  # Checking if the file is an HTML file
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        word = line.strip()
                        word_count[word] += 1

    return word_count

def main():
    if len(sys.argv) < 2:
        print("Usage: python count_top_words.py <root_directory>")
        sys.exit(1)

    root_directory = sys.argv[1]
    word_count = count_words_in_files(root_directory)
    
    # Get the top 5 most common words 
    most_common_words = word_count.most_common(5)
    
    print("Top 5 most common words:")
    for word, count in most_common_words:
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()
