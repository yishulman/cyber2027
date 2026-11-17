"""Homework 3 - Vigenere and Kasiski.

Copy this file to  students/studentXX/hw3/solution.py  and fill in the functions.
Keep the function names and parameters exactly as they are: the unit tests call them.
All texts are uppercase A-Z only, with no spaces.
"""
from pathlib import Path
from collections import Counter

# English letter frequencies in percent, A..Z
ENGLISH_FREQ = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966,
                0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987,
                6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]


def _ic(text: str) -> float:
    """Index of coincidence of a string."""
    n = len(text)
    if n < 2:
        return 0.0
    return sum(v * (v - 1) for v in Counter(text).values()) / (n * (n - 1))


def _english_score(column: str, shift: int) -> float:
    """How English-like the column looks after undoing a Caesar shift."""
    counts = Counter(column)
    total = 0.0
    for letter, n in counts.items():
        plain = (ord(letter) - 65 - shift) % 26
        total += n * ENGLISH_FREQ[plain]
    return total / len(column)



def load_ciphertext(path=None):
    """Read hw3.txt and return the ciphertext as one string of letters. (Ready - do not change.)"""
    path = Path(path) if path else Path(__file__).with_name("hw3.txt")
    lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines()]
    return "".join(l for l in lines if l and not l.startswith("#"))


def encrypt(plaintext: str, key: str) -> str:
    """Vigenere encryption.  encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR" """
    return "".join(chr((ord(p) - 65 + ord(key[i % len(key)]) - 65) % 26 + 65)
                   for i, p in enumerate(plaintext))


def decrypt(ciphertext: str, key: str) -> str:
    """The inverse of encrypt."""
    return "".join(chr((ord(c) - 65 - (ord(key[i % len(key)]) - 65)) % 26 + 65)
                   for i, c in enumerate(ciphertext))


def find_repeats(ciphertext: str, length: int = 3) -> dict[str, list[int]]:
    """Every sequence of `length` letters that appears at least twice.

    Returns {sequence: [all start positions, ascending, counted from 0]}.
    """
    positions = {}
    for i in range(len(ciphertext) - length + 1):
        positions.setdefault(ciphertext[i:i + length], []).append(i)
    return {seq: pos for seq, pos in positions.items() if len(pos) >= 2}


def guess_key_length(ciphertext: str, max_length: int = 12) -> int:
    """The most likely key length between 2 and max_length.

    Careful: if the real length is 5, then 10 also divides all the distances.
    Return the shortest length that explains the text.
    """
    # 1) Average index of coincidence of the columns for each candidate length.
    #    The true length and all its multiples score high, so take the best one.
    scores = {L: sum(_ic(ciphertext[i::L]) for i in range(L)) / L
              for L in range(2, max_length + 1)}
    best = max(scores, key=scores.get)
    # 2) Multiples of the real length also score high (5 -> 10). Return the
    #    shortest length d dividing `best` for which the recovered key really
    #    repeats with period d.
    key = recover_key(ciphertext, best)
    for d in range(2, best):
        if best % d == 0 and all(key[i] == key[i % d] for i in range(best)):
            return d
    return best


def recover_key(ciphertext: str, key_length: int) -> str:
    """Given the key length, find the key by frequency analysis of each column."""
    key = ""
    for i in range(key_length):
        column = ciphertext[i::key_length]
        best_shift = max(range(26), key=lambda k: _english_score(column, k))
        key += chr(65 + best_shift)
    return key


def break_cipher(ciphertext: str) -> tuple[str, str]:
    """Full attack with no hints. Returns (key, plaintext)."""
    key = recover_key(ciphertext, guess_key_length(ciphertext))
    return key, decrypt(ciphertext, key)


if __name__ == "__main__":
    key, plaintext = break_cipher(load_ciphertext())
    print("key:", key)
    print(plaintext[:200])
