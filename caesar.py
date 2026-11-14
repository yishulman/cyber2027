import string

ENGLISH_FREQS = {
    'a': 8.12, 'b': 1.49, 'c': 2.71, 'd': 4.32, 'e': 12.02,
    'f': 2.30, 'g': 2.03, 'h': 5.92, 'i': 7.31, 'j': 0.10,
    'k': 0.69, 'l': 3.98, 'm': 2.61, 'n': 6.95, 'o': 7.68,
    'p': 1.82, 'q': 0.11, 'r': 6.02, 's': 6.28, 't': 9.10,
    'u': 2.88, 'v': 1.11, 'w': 2.09, 'x': 0.17, 'y': 2.11,
    'z': 0.07
}

def get_letter_frequencies(text):
    text = text.lower()
    letters_only = []
    for char in text:
        if char in string.ascii_lowercase:
            letters_only.append(char)
            
    total_letters = len(letters_only)
    if total_letters == 0:
        return {}
    
    counts = {}
    for char in string.ascii_lowercase:
        counts[char] = 0
        
    for char in letters_only:
        counts[char] += 1
        
    frequencies = {}
    for char in string.ascii_lowercase:
        count = counts[char]
        percentage = (count / total_letters) * 100
        frequencies[char] = percentage
        
    return frequencies

def score_text(text):
    input_freqs = get_letter_frequencies(text)
    if not input_freqs:
        return float('inf')
    
    total_diff = 0
    for char in string.ascii_lowercase:
        input_percentage = input_freqs[char]
        standard_percentage = ENGLISH_FREQS[char]
        
        diff = abs(input_percentage - standard_percentage)
        total_diff += diff
        
    return total_diff

def english_score(text):
    error_score = score_text(text)
    if error_score == float('inf'):
        return 0.0
    
    score = 100.0 - error_score
    if score < 0.0:
        score = 0.0
        
    return round(score, 2)

def decrypt_caesar(ciphertext, shift):
    decrypted_chars = []
    for char in ciphertext:
        if char in string.ascii_lowercase:
            old_index = string.ascii_lowercase.index(char)
            new_index = (old_index - shift) % 26
            decrypted_chars.append(string.ascii_lowercase[new_index])
        elif char in string.ascii_uppercase:
            old_index = string.ascii_uppercase.index(char)
            new_index = (old_index - shift) % 26
            decrypted_chars.append(string.ascii_uppercase[new_index])
        else:
            decrypted_chars.append(char)
            
    return "".join(decrypted_chars)

def crack_caesar(ciphertext):
    best_score = -1.0
    best_text = ""
    best_shift = 0
    
    for shift in range(26):
        candidate_text = decrypt_caesar(ciphertext, shift)
        score = english_score(candidate_text)
        
        if score > best_score:
            best_score = score
            best_text = candidate_text
            best_shift = shift
            
    print("=== CAESAR CIPHER RESULT ===")
    print(f"Key/Shift found: {best_shift} (Score: {best_score}/100)")
    print(f"Decrypted Message: {best_text}\n")
    
    return best_shift, best_text

def decrypt_rail_fence(ciphertext, rails):
    if rails <= 1:
        return ciphertext
        
    pattern = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    
    for i in range(len(ciphertext)):
        pattern[rail].append(i)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
            
    rail_chars = {}
    index = 0
    for r in range(rails):
        count = len(pattern[r])
        rail_chars[r] = list(ciphertext[index:index + count])
        index += count
        
    result = []
    rail = 0
    direction = 1
    for i in range(len(ciphertext)):
        result.append(rail_chars[rail].pop(0))
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
            
    return "".join(result)

def crack_transposition(ciphertext):
    best_score = -1.0
    best_text = ""
    best_rails = 2
    
    text_length = len(ciphertext)
    max_rails = text_length // 2
    if max_rails < 2:
        max_rails = 2
    if max_rails > 20:
        max_rails = 20
        
    for rails in range(2, max_rails + 1):
        candidate_text = decrypt_rail_fence(ciphertext, rails)
        score = english_score(candidate_text)
        
        if score > best_score:
            best_score = score
            best_text = candidate_text
            best_rails = rails
            
    print("=== TRANSPOSITION CIPHER RESULT ===")
    print(f"Best Rails/Rows found: {best_rails} (Score: {best_score}/100)")
    print(f"Decrypted Message: {best_text}\n")
    
    return best_rails, best_text

crack_transposition("TO SRR OLSET  VH LER OU E HBSEETEVIAFRBDEEETD HAEV  SO A FOTEVNEJT ATRMORR E SOHATHLORMANSA UR  EYRE IO NARESC  N ANRADFNEMRLIITR TT TE AOANNHRTH AEYHLSK GEI") #i didnt manage teacher its giving me a non english sentence, ive been trying and cant get it to work
crack_caesar("OT ZNK GLZKXTUUT ZNK COTJ INGTMKJ JOXKIZOUT GTJ ZNK IRUAJY SUBKJ ZUCGXJ ZNK YKG ZNK RKZZKX GXXOBKJ ZNXKK CKKQY RGZK HKIGAYK OZ")