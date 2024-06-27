import os

def load_inverted_index_from_directory(directory_path):
    inverted_index = {}
    if not os.path.exists(directory_path):
        print("The directory does not exist.")
        return inverted_index

    if not os.path.isdir(directory_path):
        print("The provided path is not a directory. Please provide a directory path.")
        return inverted_index

    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    for line in file:
                        parts = line.strip().split(':')
                        if len(parts) == 2:
                            word = parts[0].strip()
                            documents = parts[1].strip().split(',')
                            if word in inverted_index:
                                inverted_index[word].extend([doc.strip() for doc in documents])
                            else:
                                inverted_index[word] = [doc.strip() for doc in documents]
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

    return inverted_index

def search_word(inverted_index, word):
    if word in inverted_index:
        return inverted_index[word]
    else:
        return []

def main():
    directory_path = input("Enter the path to the directory containing the inverted index files (no quotes, just the direct path to the directory): ")
    inverted_index = load_inverted_index_from_directory(directory_path)
    
    if not inverted_index:
        return
    
    while True:
        search_query = input("\nEnter a word to search (or type 'exit' to quit): ").strip()
        if search_query.lower() == 'exit':
            break
        results = search_word(inverted_index, search_query)
        if results:
            print(f"\n\nThe word '{search_query}' is found in the following documents:\n")
            for document in results:
                print(document)
        else:
            print(f"The word '{search_query}' was not found in any documents.")

if __name__ == "__main__":
    main()
