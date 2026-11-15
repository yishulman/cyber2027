"""Homework 3 - Vigenere and Kasiski.

Copy this file to  students/studentXX/hw3/solution.py  and fill in the functions.
Keep the function names and parameters exactly as they are: the unit tests call them.
All texts are uppercase A-Z only, with no spaces.
"""
from collections import Counter, defaultdict
from math import log
from pathlib import Path

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Relative frequency (in %) of each letter in English text.
ENGLISH_FREQ = [
    8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153,
    0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056,
    2.758, 0.978, 2.360, 0.150, 1.974, 0.074,
]

LOG_FREQ = [log(f / 100) for f in ENGLISH_FREQ]


def load_ciphertext(path=None):
    """Read hw3.txt and return the ciphertext as one string of letters. (Ready - do not change.)"""
    path = Path(path) if path else Path(__file__).with_name("hw3.txt")
    lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines()]
    return "".join(l for l in lines if l and not l.startswith("#"))


def _shift(text: str, key: str, sign: int) -> str:
    out = []
    k = len(key)
    for i, ch in enumerate(text):
        s = ord(key[i % k]) - 65
        out.append(chr((ord(ch) - 65 + sign * s) % 26 + 65))
    return "".join(out)


def encrypt(plaintext: str, key: str) -> str:
    """Vigenere encryption.  encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR" """
    return _shift(plaintext, key, +1)


def decrypt(ciphertext: str, key: str) -> str:
    """The inverse of encrypt."""
    return _shift(ciphertext, key, -1)


def find_repeats(ciphertext: str, length: int = 3) -> dict[str, list[int]]:
    """Every sequence of `length` letters that appears at least twice.

    Returns {sequence: [all start positions, ascending, counted from 0]}.
    """
    positions = defaultdict(list)
    for i in range(len(ciphertext) - length + 1):
        positions[ciphertext[i:i + length]].append(i)
    return {seq: pos for seq, pos in positions.items() if len(pos) >= 2}


def _english_fit(text: str) -> float:
    """Average log-probability per letter under English letter frequencies (higher = more English)."""
    return sum(LOG_FREQ[ord(c) - 65] for c in text) / len(text)


def guess_key_length(ciphertext: str, max_length: int = 12) -> int:
    """The most likely key length between 2 and max_length.

    Careful: if the real length is 5, then 10 also divides all the distances.
    Return the shortest length that explains the text.
    """
    # For each candidate length, recover the best key and see how English the
    # result looks. The true length (and every multiple of it) gives English;
    # a wrong length gives garbage in at least some columns.
    fits = {}
    for L in range(2, max_length + 1):
        key = recover_key(ciphertext, L)
        fits[L] = _english_fit(decrypt(ciphertext, key))
    best = max(fits.values())
    # Multiples of the true length fit just as well, so take the SHORTEST
    # length that is almost as good as the best one.
    for L in range(2, max_length + 1):
        if fits[L] >= best - 0.08:
            return L
    return max(fits, key=fits.get)


def _best_shift(column: str) -> int:
    """The shift (0-25) that makes the column look most like English (chi-squared)."""
    n = len(column)
    counts = Counter(column)
    best_shift, best_chi = 0, float("inf")
    for shift in range(26):
        chi = 0.0
        for letter in range(26):
            observed = counts.get(ALPHABET[(letter + shift) % 26], 0)
            expected = ENGLISH_FREQ[letter] / 100 * n
            chi += (observed - expected) ** 2 / expected
        if chi < best_chi:
            best_shift, best_chi = shift, chi
    return best_shift


def recover_key(ciphertext: str, key_length: int) -> str:
    """Given the key length, find the key by frequency analysis of each column."""
    return "".join(ALPHABET[_best_shift(ciphertext[i::key_length])] for i in range(key_length))


def _shorten_key(key: str) -> str:
    """If the key is a repetition of a shorter word (e.g. ABCABC), return the short word."""
    for d in range(1, len(key)):
        if len(key) % d == 0 and key[:d] * (len(key) // d) == key:
            return key[:d]
    return key


def break_cipher(ciphertext: str) -> tuple[str, str]:
    """Full attack with no hints. Returns (key, plaintext)."""
    length = guess_key_length(ciphertext)
    key = _shorten_key(recover_key(ciphertext, length))
    return key, decrypt(ciphertext, key)


if __name__ == "__main__":
    key, plaintext = break_cipher(load_ciphertext())
    print("key:", key)
    print(plaintext[:200])
