import random

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
    
    low_text = text.lower().split()
    if len(low_text) == 0:
        return 0
        
    matches = 0
    for i in low_text:
        if i in common_words:
            matches += 1

    return matches / len(low_text)


def decrypt_caesar(text, shift):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    new_sentence = ""

    for i in text:
        if i.lower() in alphabet:
            old = alphabet.index(i.lower())
            new = (old - shift) % 26
            new_sentence += alphabet[new]
        else:
            new_sentence += i
            
    return new_sentence


def encrypt_caesar(text, shift):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    new_sentence = ""

    for i in text:
        if i.lower() in alphabet:
            old = alphabet.index(i.lower())
            new = (old + shift) % 26
            new_sentence += alphabet[new]
        else:
            new_sentence += i
            
    return new_sentence


def break_caesar(text):
    _max = -1
    max_num = ""
    best_shift = 0

    for i in range(1, 26):
        a = decrypt_caesar(text, i)
        b = english_score(a)
        if b > _max:
            _max = b
            max_num = a
            best_shift = i

    return best_shift, max_num


def generate_random_english_text(length):
    words = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog", "hello", "world", "cyber", "security"]
    text = ""
    while len(text) < length:
        text += random.choice(words) + " "
    return text[:length].strip()


lengths = [5, 10, 20, 50, 100]
trials = 30

for length in lengths:
    success_count = 0
    
    for _ in range(trials):
        original_text = generate_random_english_text(length)
        shift = random.randint(1, 25)
        encrypted_text = encrypt_caesar(original_text, shift)
        
        decrypted_text = break_caesar(encrypted_text)
        
        if decrypted_text.lower() == original_text.lower():
            success_count += 1
            
    success_rate = (success_count / trials) * 100
    print(success_rate)


