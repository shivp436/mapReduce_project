import os
import random

# Create data folder
os.makedirs("data", exist_ok=True)

# Word list
words = ["apple", "banana", "orange", "grape", "kiwi", "mango", "peach"]

# File generation
for i in range(1, 16):  # Files 01_words to 15_words
    file_name = f"data/{i:02d}_words.txt"
    print(f"Writing File {file_name}")
    with open(file_name, 'w') as f:
        for _ in range(170_000):  # ~170k lines per file (~100MB)
            line = " ".join(random.choices(words, k=100))
            f.write(line + "\n")

print("Files generated.")
