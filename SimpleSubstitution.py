from src.hacker_tools import *
from pycipher import *
import random

# -----------------------------
# Step 0 — Load ciphertext
# -----------------------------
with open('enc/SimpleSubstitution.txt', 'r') as f:
    ciphertext = f.read()

# -----------------------------
# Step 1 — Initial frequency-based key
# -----------------------------
freq = calculate_letters_frequencies(ciphertext)
sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
sorted_English_freq = sorted(ENGLISH_FREQ.items(), key=lambda x: x[1], reverse=True)

LIST_text = list(sorted_freq)
LIST_En = list(sorted_English_freq)

LIST_En_letters = [t[0] for t in LIST_En] 
LIST_text_letters = [t[0] for t in sorted_freq] 

current_key = ""


for i in range(0, 26):
    letter = LETTERS[i]
    index =  LIST_En_letters.index(letter)
    current_key += LIST_text_letters[index]
print(current_key)

plaintext = SimpleSubstitution(current_key.upper()).decipher(ciphertext)


with open("enc/DE1_SimpleSubstitution.txt", "w") as f:
    f.write(plaintext)
trigrmas = get_top_trigrams(plaintext, 50)

brown_trigrams = get_brown_top_trigrams(50)
shared = compare_trigrams(trigrmas, brown_trigrams)

print(shared)
