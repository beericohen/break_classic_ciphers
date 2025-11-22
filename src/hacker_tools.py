from collections import Counter
import nltk

def get_top_trigrams(text, n=200):

    # Remove non-alphabetic characters and create trigrams
    text = ''.join(c for c in text.lower() if c.isalpha())
    trigrams = [text[i:i+3] for i in range(len(text) - 2)]
    
    # Count and return top n trigrams
    counter = Counter(trigrams)
    return counter.most_common(n)

def get_brown_top_trigrams(n=200):
    nltk.download('brown')
    from nltk.corpus import brown
    brown_text = ' '.join(word.lower() for word in brown.words() if word.isalpha())
    return get_top_trigrams(brown_text, n)

def compare_trigrams(trigrams1, trigrams2):
    """Compare how many trigrams are shared between two lists of top trigrams."""
    set1 = set(trigram for trigram, count in trigrams1)
    set2 = set(trigram for trigram, count in trigrams2)
    shared = set1.intersection(set2)
    return shared

ENGLISH_FREQ = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702,
    'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153,
    'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507,
    'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 'y': 0.01974,
    'z': 0.00074
}

LETTERS = 'abcdefghijklmnopqrstuvwxyz'

def chi_squared_score(text_freq, eng_freq):
    score = 0.0
    for letter in LETTERS:
        observed = text_freq[letter]
        expected = eng_freq[letter]
        if expected > 0:
            score += ((observed - expected) ** 2) / expected
    return score

def calculate_letters_frequencies(text):
        """Calculate the frequency ratio of each letter in the given text."""
        # Count only alphabetic characters
        clean_text = ''.join(c.lower() for c in text if c.isalpha())
        total_letters = len(clean_text)
        
        if total_letters == 0:
            return {letter: 0.0 for letter in LETTERS}
        
        letter_counts = Counter(clean_text)
        
        # Calculate frequency ratios
        frequency_ratios = {}
        for letter in LETTERS:
            frequency_ratios[letter] = letter_counts.get(letter, 0) / total_letters
        
        return frequency_ratios



if __name__ == "__main__":
    # Example text
    sample_text = "The quick brown fox jumps over the lazy dog. This is a sample text for demonstration purposes."
            
    # Calculate letter frequencies
    print("Letter Frequencies:")
    freq = calculate_letters_frequencies(sample_text)
    for letter, ratio in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {letter}: {ratio:.4f}")
    
    # Chi-squared score
    chi_score = chi_squared_score(freq, ENGLISH_FREQ)
    print(f"\nChi-squared score: {chi_score:.4f}")
    
    # Top trigrams
    print("\nTop 10 trigrams in sample text:")
    top_trigrams = get_top_trigrams(sample_text, 10)
    for trigram, count in top_trigrams:
        print(f"  {trigram}: {count}")
    
    # Compare with Brown corpus
    print("\nComparing with Brown corpus trigrams...")
    brown_trigrams = get_brown_top_trigrams(50)
    shared = compare_trigrams(top_trigrams, brown_trigrams)
    print(f"  Shared trigrams: {shared}")