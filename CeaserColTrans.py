from src.hacker_tools import *
from itertools import permutations
from pycipher import Caesar

# --- Load ciphertext ---
with open('enc/Caesar_ColTrans.txt', 'r') as f:
    ciphertext = f.read().replace("\n", "")

key_length = 5


best_score1 = float('inf')
best_shift = 0
best_caesar_text = ""

for shift in range(26):
    decrypted = Caesar(shift).decipher(ciphertext)
    freq = calculate_letters_frequencies(decrypted)
    score = chi_squared_score(freq, ENGLISH_FREQ)
    if score < best_score1:
        best_score1 = score
        best_shift = shift
        best_caesar_text = decrypted

total_len = len(best_caesar_text)
num_full_rows = total_len // key_length
extra_chars = total_len % key_length

# Columns lengths: first 'extra_chars' columns are longer
col_lengths = [
    num_full_rows + 1 if i < extra_chars else num_full_rows
    for i in range(key_length)
]

columns = []
j = 0
for length in col_lengths:
    columns.append(best_caesar_text[j:j + length])
    j += length

english_trigrams = get_brown_top_trigrams(200)

def reconstruct(columns, order):
    max_len = max(len(c) for c in columns)
    out = []

    for r in range(max_len):
        for col_index in order:
            col = columns[col_index]
            if r < len(col):
                out.append(col[r])

    return "".join(out)

results = []

for perm in permutations(range(key_length)):
    text = reconstruct(columns, perm)

    score = compare_trigrams(get_top_trigrams(text, 200), english_trigrams)

    results.append((score, perm, text))

results.sort(key=lambda x: x[0], reverse=True)

# --- Print top 3 candidates ---
for i in range(3):
    score, perm, text = results[i]
    print(f"\n=== Candidate {i+1} ===")
    print(f"Order: {perm}")
    print(f"Score: {score}")
    print(text)
