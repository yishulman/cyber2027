#!/usr/bin/env python3
"""
פריצת צופן ויז'נר (Vigenère) בשיטת Kasiski + ניתוח שכיחויות.

שלבים:
1. חיפוש דפוסים (n-grams) שחוזרים בטקסט המוצפן.
2. חישוב המרחקים בין ההופעות של כל דפוס.
3. מציאת המחלק המשותף של המרחקים -> אורך המפתח.
4. סידור הטקסט במערך דו-ממדי: שורה i מכילה את כל האותיות באינדקסים i, i+k, i+2k...
5. בכל שורה (שכולה הוצפנה באותו מפתח-אות, כלומר צופן קיסר) בחירת ההזזה
   שמתאימה ביותר להתפלגות האותיות הנפוצה באנגלית (מבחן chi-squared).

שימוש:
    python vigenere_breaker.py ciphertext.txt
"""
import sys
from collections import defaultdict, Counter
from functools import reduce
from math import gcd

# התפלגות אותיות באנגלית (באחוזים) A..Z
ENGLISH_FREQ = [
    8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153,
    0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056,
    2.758, 0.978, 2.360, 0.150, 1.974, 0.074,
]
A = ord("A")


def clean(text):
    """משאיר רק אותיות לטיניות באותיות גדולות."""
    return "".join(c for c in text.upper() if "A" <= c <= "Z")


# ---------- שלב 1+2: דפוסים חוזרים ומרחקים ----------
def find_repeat_distances(text, min_len=3, max_len=6):
    distances = []
    for n in range(min_len, max_len + 1):
        positions = defaultdict(list)
        for i in range(len(text) - n + 1):
            positions[text[i:i + n]].append(i)
        for pos in positions.values():
            if len(pos) > 1:
                # מרחק בין כל זוג הופעות עוקבות
                distances.extend(b - a for a, b in zip(pos, pos[1:]))
    return distances


# ---------- שלב 3: מחלק משותף ----------
def divisors(n, max_k):
    return [d for d in range(2, min(n, max_k) + 1) if n % d == 0]


def candidate_key_lengths(distances, max_k=20):
    """
    מחזיר רשימת אורכי מפתח אפשריים לפי תדירות המחלקים של המרחקים,
    ואת ה-GCD של כל המרחקים (שבדרך כלל מתקלקל ע"י רעש, ולכן לא מסתמכים רק עליו).
    """
    if not distances:
        return [], 0
    overall_gcd = reduce(gcd, distances)
    votes = Counter()
    for d in distances:
        for div in divisors(d, max_k):
            votes[div] += 1
    return [k for k, _ in votes.most_common()], overall_gcd


def index_of_coincidence(s):
    n = len(s)
    if n < 2:
        return 0
    counts = Counter(s)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1))


def pick_key_length(text, candidates, max_k=20):
    """בין המועמדים בוחר את האורך שנותן IC ממוצע הכי קרוב לאנגלית (~0.066)."""
    if not candidates:
        candidates = list(range(1, max_k + 1))
    scores = {}
    for k in sorted(set(candidates[:10])):
        rows = build_matrix(text, k)
        scores[k] = sum(index_of_coincidence(r) for r in rows) / k
    top = max(scores.values())
    # כפולות של אורך המפתח נותנות IC דומה, לכן בוחרים את הקטן ביותר
    # מבין אלה שקרובים לציון הטוב ביותר.
    return min(k for k, s in scores.items() if s >= top - 0.008)


def minimal_period(key):
    """מקצר מפתח שהוא חזרה של תת-מחרוזת (CRYPTOCRYPTO -> CRYPTO)."""
    for p in range(1, len(key) + 1):
        if len(key) % p == 0 and key[:p] * (len(key) // p) == key:
            return key[:p]
    return key


# ---------- שלב 4: מערך דו-ממדי ----------
def build_matrix(text, k):
    """שורה i = כל האותיות שהאינדקס שלהן ≡ i (mod k)."""
    return [text[i::k] for i in range(k)]


# ---------- שלב 5: מציאת ההזזה בכל שורה ----------
def best_shift(row):
    n = len(row)
    counts = Counter(row)
    best, best_chi = 0, float("inf")
    for shift in range(26):
        chi = 0.0
        for letter in range(26):
            # האות האמיתית 'letter' מוצפנת ל-(letter+shift)
            observed = counts.get(chr(A + (letter + shift) % 26), 0)
            expected = ENGLISH_FREQ[letter] / 100 * n
            chi += (observed - expected) ** 2 / expected
        if chi < best_chi:
            best, best_chi = shift, chi
    return best


def find_key(rows):
    return "".join(chr(A + best_shift(r)) for r in rows)


def decrypt(text, key):
    out = []
    for i, c in enumerate(text):
        out.append(chr((ord(c) - ord(key[i % len(key)])) % 26 + A))
    return "".join(out)


def crack(ciphertext, max_k=20, verbose=True):
    text = clean(ciphertext)
    distances = find_repeat_distances(text)
    candidates, g = candidate_key_lengths(distances, max_k)
    k = pick_key_length(text, candidates, max_k)
    rows = build_matrix(text, k)
    key = minimal_period(find_key(rows))
    plain = decrypt(text, key)
    if verbose:
        print(f"Text length: {len(text)} | Distances found: {len(distances)}")
        print(f"GCD of all distances: {g}")
        print(f"Candidate key lengths (by most common divisors): {candidates[:8]}")
        print(f"Chosen key length: {k}")
        print(f"Key: {key}")
        print(f"Decrypted text (beginning): {plain[:200]}")
    return key, plain


def read_ciphertext_from_user():
    """קורא טקסט מוצפן שהמשתמש מדביק/מקליד. מסיימים בשורה ריקה (Enter פעמיים)."""
    print("Paste the ciphertext here (multiple lines are allowed).")
    print("When finished, press Enter on an empty line:\n")
    lines = []
    try:
        while True:
            line = input()
            if line.strip() == "" and lines:
                break
            lines.append(line)
    except EOFError:
        pass
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        # אם הועבר קובץ כארגומנט - קוראים ממנו
        with open(sys.argv[1], encoding="utf-8") as f:
            ciphertext = f.read()
    else:
        # אחרת - מבקשים מהמשתמש להקליד/להדביק את הצופן
        ciphertext = read_ciphertext_from_user()

    if not clean(ciphertext):
        print("No ciphertext was received.")
        sys.exit(1)
    print()
    crack(ciphertext)