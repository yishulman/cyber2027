from collections import Counter
import random

ENGLISH_FREQS = {
    'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95,
    'S': 6.28, 'R': 6.02, 'H': 5.92, 'D': 4.32, 'L': 3.98, 'U': 2.88,
    'C': 2.71, 'M': 2.61, 'F': 2.30, 'Y': 2.11, 'W': 2.09, 'G': 2.03,
    'P': 1.82, 'B': 1.49, 'V': 1.11, 'K': 0.69, 'X': 0.17, 'Q': 0.11,
    'J': 0.10, 'Z': 0.07
}

# מילון מצומצם של מילות נפוצות באנגלית לבדיקת תקינות צופן העמודות
ENGLISH_WORDS = {
    "THE", "BE", "TO", "OF", "AND", "A", "IN", "THAT", "HAVE", "I", "IT", "FOR", "NOT", "ON", "WITH",
    "HE", "AS", "YOU", "DO", "AT", "THIS", "BUT", "HIS", "BY", "FROM", "THEY", "WE", "SAY", "HER",
    "SHE", "OR", "AN", "WILL", "MY", "ONE", "ALL", "WOULD", "THERE", "THEIR", "WHAT", "SO", "UP",
    "OUT", "IF", "ABOUT", "WHO", "GET", "WHICH", "GO", "ME", "WHEN", "MAKE", "CAN", "LIKE", "TIME",
    "NO", "JUST", "HIM", "KNOW", "TAKE", "PEOPLE", "INTO", "YEAR", "YOUR", "GOOD", "SOME", "COULD",
    "THEM", "SEE", "OTHER", "THAN", "THEN", "NOW", "LOOK", "ONLY", "COME", "ITS", "OVER", "THINK",
    "ALSO", "BACK", "AFTER", "USE", "TWO", "HOW", "OUR", "WORK", "FIRST", "WELL", "WAY", "EVEN",
    "NEW", "WANT", "BECAUSE", "ANY", "THESE", "GIVE", "DAY", "MOST", "US", "HATE", "ENEMY", "AGENTS",
    "INTERCEPT", "MESSAGES", "SOON", "GIVE", "UP", "WILL", "BE", "OVER"
}

def english_score(text):
    text = text.upper()
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    counts = Counter(letters)
    total = len(letters)
    score = 0.0
    for char, freq in ENGLISH_FREQS.items():
        observed_freq = (counts.get(char, 0) / total) * 100
        score += observed_freq * freq
    return score

def decrypt_caesar(ciphertext, shift):
    plain = []
    for c in ciphertext:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            plain.append(chr((ord(c) - base - shift) % 26 + base))
        else:
            plain.append(c)
    return "".join(plain)

def break_caesar(ciphertext):
    best_score = -1
    best_text = ""
    best_shift = 0
    for shift in range(26):
        decoded = decrypt_caesar(ciphertext, shift)
        score = english_score(decoded)
        if score > best_score:
            best_score = score
            best_text = decoded
            best_shift = shift
    return best_shift, best_text

def decrypt_transposition(ciphertext, key_len):
    n = len(ciphertext)
    num_rows = n // key_len
    remainder = n % key_len
    
    col_lens = []
    for i in range(key_len):
        if i < remainder:
            col_lens.append(num_rows + 1)
        else:
            col_lens.append(num_rows)
            
    cols = []
    curr = 0
    for c_len in col_lens:
        cols.append(ciphertext[curr:curr + c_len])
        curr += c_len
        
    plain_chars = []
    max_rows = max(col_lens)
    for r in range(max_rows):
        for c in range(key_len):
            if r < len(cols[c]):
                plain_chars.append(cols[c][r])
                
    return "".join(plain_chars)

def count_dictionary_words(text):
    # סופרת כמה מילים מתוך הטקסט המפוענח קיימות במילון המילים האנגלי
    words = text.upper().split()
    count = 0
    for word in words:
        clean_word = "".join(c for c in word if c.isalpha())
        if clean_word in ENGLISH_WORDS:
            count += 1
    return count

def break_transposition(ciphertext):
    best_word_count = -1
    best_text = ""
    best_key_len = 0
    n = len(ciphertext)
    
    # בדיקת כל אורכי המפתח האפשריים (מספר עמודות)
    for key_len in range(2, min(n, 20)):
        candidate = decrypt_transposition(ciphertext, key_len)
        word_count = count_dictionary_words(candidate)
        
        if word_count > best_word_count:
            best_word_count = word_count
            best_text = candidate
            best_key_len = key_len
            
    return best_key_len, best_text

def encrypt_caesar(text, shift):
    plain = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            plain.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            plain.append(c)
    return "".join(plain)

def run_experiment():
    corpus = (
        "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG "
        "CRYPTOGRAPHY IS THE PRACTICE AND STUDY OF TECHNIQUES FOR SECURE COMMUNICATION "
        "IN THE PRESENCE OF ADVERSARIAL THIRD PARTIES MORE GENERALLY CRYPTOGRAPHY IS ABOUT "
        "CONSTRUCTING AND ANALYZING PROTOCOLS THAT PREVENT THIRD PARTIES OR THE PUBLIC FROM "
        "READING PRIVATE MESSAGES MODERN CRYPTOGRAPHY EXISTS AT THE INTERSECTION OF MATHEMATICS "
        "COMPUTER SCIENCE ELECTRICAL ENGINEERING AND OTHER DISCIPLINE"
    )
    
    lengths = [5, 10, 20, 50, 100]
    num_trials = 30

    print("=== Caesar Breaker Accuracy Experiment (30 Trials per Length) ===")
    for l in lengths:
        correct = 0
        for _ in range(num_trials):
            start = random.randint(0, len(corpus) - l)
            original = corpus[start:start + l]
            true_shift = random.randint(1, 25)
            
            ciphertext = encrypt_caesar(original, true_shift)
            predicted_shift, _ = break_caesar(ciphertext)
            
            if predicted_shift == true_shift:
                correct += 1
                
        acc = (correct / num_trials) * 100
        print(f"Length {l:3d} chars: {acc:.1f}% accuracy ({correct}/{num_trials} correct)")

if __name__ == "__main__":
    caesar_cipher = "ZNK ZKGS CUT ZNK SGZIN OT ZNK RGYZ SOTAZK GLZKX G RUTM GTJ JOLLOIARZ YKIUTJ NGRL YZAJKTZY CNU VXGIZOIK G ROZZRK KBKXE JGE AYAGRRE"
    transposition_cipher = "WHHN HN ETRINEMGOSNETRNCHTHHETTTI SSHELIVO LH DHBDKEHEE S HLTT E  GERTDEW EO E ENL OEDOOB UMHRNH RAT RCDWR IWU RLRYFNITYIEFMLOH H E TGETCEDI ITD  N IAK AAETAT"

    print("=== Decryption Results for student10 ===")
    shift, caesar_plain = break_caesar(caesar_cipher)
    print(f"Caesar Shift: {shift} | Plaintext: {caesar_plain}")

    key_len, trans_plain = break_transposition(transposition_cipher)
    print(f"Transposition Key Length (Number of Columns): {key_len} | Plaintext: {trans_plain}\n")

    run_experiment()
