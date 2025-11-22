from caesar_encrypt import *
from pycipher import *
from src.hacker_tools import *

# --- Load ciphertext ---
with open('enc/Autokey.txt', 'r') as f:
    ciphertext = f.read().replace("\n", "")

key_length = 5

parentKey = "AAAAA"

count = 0

for i in range(0,key_length):
    freq = calculate_letters_frequencies(Autokey(parentKey).decipher(ciphertext))
    score = chi_squared_score(freq, ENGLISH_FREQ)

    for j in range(0,26):
            newLetter = caesar_encrypt(parentKey[i], j)
            newKey = parentKey[:i] + newLetter + parentKey[i+1:]
            newFreq = calculate_letters_frequencies(Autokey(newKey).decipher(ciphertext))
            newScore = chi_squared_score(newFreq, ENGLISH_FREQ)

            if newScore<score:
                score = newScore
                parentKey = newKey

            count+=1
            print(count)


    print(parentKey)