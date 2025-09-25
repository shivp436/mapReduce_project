import os
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

def count_words_in_file(file_path):
    word_count = defaultdict(int)
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().lower().split()
            for word in words:
                word_count[word] += 1
    return word_count

def merge_counts(counts_list):
    total_count = defaultdict(int)
    for partial_count in counts_list:
        for word, count in partial_count.items():
            total_count[word] += count
    return total_count

def parallel_word_count(directory, num_workers=10):
    files = [os.path.join(directory, f) for f in sorted(os.listdir(directory)) if os.path.isfile(os.path.join(directory, f))]

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(count_words_in_file, files))

    total_counts = merge_counts(results)
    return total_counts

if __name__ == "__main__":
    import sys

    dir_path = sys.argv[1] if len(sys.argv) > 1 else "data"

    if not os.path.exists(dir_path):
        print(f"Directory '{dir_path}' does not exist.")
        exit(1)

    start_time = time.time()
    total_counts = parallel_word_count(dir_path)
    end_time = time.time()

    # Print all words with counts
    for word, count in sorted(total_counts.items()):
        print(f"{word}: {count}")

    print(f"\nTotal unique words: {len(total_counts)}")
    print(f"Total runtime: {end_time - start_time:.2f} seconds")

