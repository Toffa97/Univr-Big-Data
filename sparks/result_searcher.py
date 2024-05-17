import os

def load_inverted_index(file_path):
    inverted_index = {}
    if not os.path.exists(file_path):
        print("Index file does not exist.")
        return inverted_index

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                word = parts[0].strip()
                documents = parts[1].strip().split(',')
                inverted_index[word] = [doc.strip() for doc in documents]

    return inverted_index

def search_word(inverted_index, word):
    if word in inverted_index:
        return inverted_index[word]
    else:
        return []

def main():
    index_file_path = input("Enter the path to the inverted index file (no quotes, just the direct path to the index): ")
    inverted_index = load_inverted_index(index_file_path)
    
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
