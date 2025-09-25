import os
import time
from collections import defaultdict

def count_words_in_file(file_path):
    word_count = defaultdict(int)
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().lower().split()
            for word in words:
                word_count[word] += 1
    return word_count

def merge_counts(total_count, file_count):
    for word, count in file_count.items():
        total_count[word] += count

def count_words_in_directory(directory):
    total_word_count = defaultdict(int)
    
    for file_name in sorted(os.listdir(directory)):
        file_path = os.path.join(directory, file_name)

        if os.path.isfile(file_path):
            file_count = count_words_in_file(file_path)
            merge_counts(total_word_count, file_count)

    return total_word_count

if __name__ == "__main__":
    import sys

    dir_path = sys.argv[1] if len(sys.argv) > 1 else "data"

    if not os.path.exists(dir_path):
        print(f"Directory '{dir_path}' does not exist.")
        exit(1)

    start_time = time.time()
    total_counts = count_words_in_directory(dir_path)
    end_time = time.time()

    # Print all words with counts
    for word, count in sorted(total_counts.items()):
        print(f"{word}: {count}")

    print(f"\nTotal unique words: {len(total_counts)}")
    print(f"Total runtime: {end_time - start_time:.2f} seconds")

