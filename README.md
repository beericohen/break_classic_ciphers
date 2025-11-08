# break_classic_ciphers

A collection of tools for analyzing and breaking classic cryptographic ciphers.

## Overview

This repository contains homework assignments focused on breaking various classic ciphers. The encrypted files are located in the `enc/` folder, and cryptanalysis tools are provided in `src/hacker_tools.py`.

## Encrypted Files

The `enc/` folder contains the following ciphered texts to decrypt:

- `Autokey.txt` - Autokey cipher (Key length: 5)
- `Caesar_ColTrans.txt` - Caesar cipher combined with Columnar Transposition
- `ColTrans.txt` - Columnar Transposition cipher (Key length: 5)
- `SimpleSubstitution.txt` - Simple Substitution cipher

**Note:** Where relevant, the key length is **5**.

## Hacker Tools

The `src/hacker_tools.py` module provides several cryptanalysis functions:

### Trigram Analysis

#### `get_top_trigrams(text, n=200)`
Extracts the most common trigrams (3-letter sequences) from a text.

**Use case:** Trigrams are useful for identifying patterns in ciphertext. Common English trigrams like "the", "and", "ing" can help identify correct decryptions or analyze transposition ciphers.

**Parameters:**
- `text`: The text to analyze
- `n`: Number of top trigrams to return (default: 200)

**Returns:** List of tuples `(trigram, count)` sorted by frequency

#### `get_brown_top_trigrams(n=200)`
Gets the most common trigrams from the Brown corpus (standard English text).

**Use case:** Compare ciphertext trigrams against expected English trigrams to evaluate if a decryption attempt is successful.

**Parameters:**
- `n`: Number of top trigrams to return (default: 200)

**Returns:** List of tuples `(trigram, count)` from Brown corpus

#### `compare_trigrams(trigrams1, trigrams2)`
Compares two lists of trigrams and counts how many are shared.

**Use case:** Measure similarity between your decrypted text and standard English. Higher overlap suggests a more successful decryption.

**Parameters:**
- `trigrams1`: First list of trigrams (from `get_top_trigrams`)
- `trigrams2`: Second list of trigrams (from `get_brown_top_trigrams`)

**Returns:** Integer count of shared trigrams

### Frequency Analysis

#### `calculate_letters_frequencies(text)`
Calculates the frequency distribution of letters in the given text.

**Use case:** Essential for breaking substitution ciphers. Compare letter frequencies in ciphertext with known English frequencies to map cipher letters to plaintext letters.

**Parameters:**
- `text`: The text to analyze

**Returns:** Dictionary mapping each letter to its frequency ratio (0.0 to 1.0)

#### `chi_squared_score(text_freq, eng_freq)`
Calculates the chi-squared statistic comparing text frequencies to expected frequencies.

**Use case:** Quantitatively measure how closely a text matches English letter distribution. Lower scores indicate better matches. Useful for:
- Testing different Caesar cipher shifts
- Evaluating decryption attempts
- Finding the correct key length in polyalphabetic ciphers

**Parameters:**
- `text_freq`: Dictionary of observed letter frequencies (from `calculate_letters_frequencies`)
- `eng_freq`: Dictionary of expected letter frequencies (use `ENGLISH_FREQ`)

**Returns:** Chi-squared score (float) - lower is better

### Constants

#### `ENGLISH_FREQ`
Dictionary containing the expected frequency of each letter in standard English text.

**Use case:** Reference data for frequency analysis and chi-squared tests.

## Usage Example

```python
from src.hacker_tools import *

# Read encrypted text
with open('enc/SimpleSubstitution.txt', 'r') as f:
    ciphertext = f.read()

# Analyze letter frequencies
cipher_freq = calculate_letters_frequencies(ciphertext)

# Compare with English frequencies
score = chi_squared_score(cipher_freq, ENGLISH_FREQ)
print(f"Chi-squared score: {score}")

# Analyze trigrams
cipher_trigrams = get_top_trigrams(ciphertext, 50)
english_trigrams = get_brown_top_trigrams(50)
shared = compare_trigrams(cipher_trigrams, english_trigrams)
print(f"Shared trigrams: {shared}/50")
```

## Installation

```bash
pip install -r requirements.txt
```

## Approach for Each Cipher

### Simple Substitution
1. Use `calculate_letters_frequencies()` to find letter distribution
2. Map letters to the expected ENGLISH_FREQ 
4. Decipher and look for patterns in desiphered text and refine selection

### Caesar + Columnar Transposition
1. Try all 26 Caesar shifts
2. For each shift, use `chi_squared_score()` to evaluate
3. Once Caesar is broken, analyze for columnar transposition patterns
4. Try different column arrangements (key length = 5)

### Columnar Transposition
1. Key length is 5, so arrange text in 5 columns
2. Try different column permutations
3. Use `get_top_trigrams()` and `compare_trigrams()` to validate correct arrangement

### Autokey
1. Key length is 5, so try different 5-letter keys.
2. Use `calculate_letters_frequencies()` to find letter distribution for each on the 1/5 segments
3. Use `chi_squared_score()` to evaluate each attempt
4. Look for readable text patterns

## License

See LICENSE file for details.

