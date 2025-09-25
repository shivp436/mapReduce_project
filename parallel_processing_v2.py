import os
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

CHUNK_SIZE_MB = 50 * 1024 * 1024  # 50MB


def generate_chunks(file_path):
    file_size = os.path.getsize(file_path)
    mid_point = file_size // 2

    with open(file_path, 'rb') as f:
        # Chunk 1: start from 0 to adjusted mid_point
        f.seek(mid_point)
        f.readline()  # move to the end of the current line to avoid splitting word
        split_pos = f.tell()

    return [
        (file_path, 0, split_pos),
        (file_path, split_pos, file_size)
    ]


def count_words_in_chunk(args):
    file_path, start, end = args
    word_count = defaultdict(int)

    with open(file_path, 'rb') as f:
        f.seek(start)
        bytes_to_read = end - start
        data = f.read(bytes_to_read)

    text = data.decode('utf-8', errors='ignore')
    words = text.strip().lower().split()
    for word in words:
        word_count[word] += 1

    return word_count


def merge_counts(counts_list):
    total_count = defaultdict(int)
    for partial_count in counts_list:
        for word, count in partial_count.items():
            total_count[word] += count
    return total_count


def parallel_word_count(directory, num_workers=30):
    chunk_args = []

    # Generate 2 chunks per file
    for file_name in sorted(os.listdir(directory)):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            chunk_args.extend(generate_chunks(file_path))  # adds 2 chunks per file

    print(f"Total {num_workers} workers")
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(count_words_in_chunk, chunk_args))

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

    for word, count in sorted(total_counts.items()):
        print(f"{word}: {count}")

    print(f"\nTotal unique words: {len(total_counts)}")
    print(f"Total runtime: {end_time - start_time:.2f} seconds")

