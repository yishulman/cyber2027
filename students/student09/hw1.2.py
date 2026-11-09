import math

def english_score(text):
    common_words = {
            "the", "of", "to", "and", "a", "in", "is", "it", "you", "that", 
            "he", "was", "for", "on", "are", "with", "as", "i", "his", "they", 
            "be", "at", "one", "have", "this", "from", "or", "had", "by", "hot", 
            "but", "some", "what", "there", "we", "can", "out", "other", "were", "all", 
            "your", "when", "up", "use", "word", "how", "said", "an", "each", "she", 
            "which", "do", "their", "time", "if", "will", "way", "about", "many", "then", 
            "them", "would", "write", "like", "so", "these", "her", "long", "make", "thing", 
            "see", "him", "two", "has", "look", "more", "day", "could", "go", "come", 
            "did", "my", "sound", "no", "most", "number", "who", "over", "know", "water", 
            "than", "call", "first", "people", "may", "down", "side", "been", "now", "find",
            "any", "new", "work", "part", "take", "get", "place", "made", "live", "where", 
            "after", "back", "little", "only", "round", "man", "year", "came", "show", "every", 
            "good", "me", "give", "our", "under", "name", "very", "through", "just", "form", 
            "much", "great", "think", "say", "help", "low", "line", "before", "turn", "cause", 
            "same", "mean", "differ", "move", "right", "boy", "old", "too", "does", "tell", 
            "sentence", "set", "three", "want", "air", "well", "also", "play", "small", "end", 
            "put", "home", "read", "hand", "port", "large", "spell", "add", "even", "land", 
            "here", "must", "big", "high", "such", "follow", "act", "why", "ask", "men", 
            "change", "went", "light", "kind", "off", "need", "house", "picture", "try", "us", 
            "again"
        }
    
    words = text.lower().split()
    if not words:
        return 0
        
    matches = 0
    for w in words:
        if w in common_words:
            matches += 1

    return matches / len(words)


def decrypt_transposition(ciphertext, cols):
    n = len(ciphertext)
    num_rows = math.ceil(n / cols)
    full_cols = n % cols
    if full_cols == 0:
        full_cols = cols

    col_starts = []
    current_idx = 0
    for c in range(cols):
        col_starts.append(current_idx)
        if c < full_cols:
            col_length = num_rows
        else:
            col_length = num_rows - 1
        current_idx += col_length

    plaintext = ""
    for r in range(num_rows):
        for c in range(cols):
            if c < full_cols:
                col_length = num_rows
            else:
                col_length = num_rows - 1
                
            if r < col_length:
                plaintext += ciphertext[col_starts[c] + r]

    return plaintext


def break_transposition(text):
    best_score = -1
    best_cols = None
    best_plaintext = ""

    for cols in range(2, len(text)):
        candidate = decrypt_transposition(text, cols)
        score = english_score(candidate)
        
        if score > best_score:
            best_score = score
            best_cols = cols
            best_plaintext = candidate

    return best_cols, best_plaintext


