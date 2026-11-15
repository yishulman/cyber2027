#!/usr/bin/env python3
"""
Caesar cipher breaker using English letter frequencies.

For each of the 26 possible shifts, the text is decrypted and its letter
distribution is compared to the typical English distribution using a
chi-squared test. The shift with the lowest score is the most likely key.

Usage:
    python caesar_breaker.py              (paste the ciphertext when asked)
    python caesar_breaker.py cipher.txt   (read the ciphertext from a file)
"""
import sys
from collections import Counter

# Typical English letter frequencies (percent), A..Z
ENGLISH_FREQ = [
    8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153,
    0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056,
    2.758, 0.978, 2.360, 0.150, 1.974, 0.074,
]
A = ord("A")


def clean(text):
    """Keep only Latin letters, uppercased."""
    return "".join(c for c in text.upper() if "A" <= c <= "Z")


def chi_squared(text, shift):
    """Score of the text decrypted with the given shift (lower = more English-like)."""
    n = len(text)
    counts = Counter(text)
    score = 0.0
    for letter in range(26):
        # The real letter 'letter' was encrypted to (letter + shift) % 26
        observed = counts.get(chr(A + (letter + shift) % 26), 0)
        expected = ENGLISH_FREQ[letter] / 100 * n
        score += (observed - expected) ** 2 / expected
    return score


def decrypt(text, shift):
    """Decrypt the original text, keeping case and non-letter characters."""
    out = []
    for c in text:
        if "A" <= c <= "Z":
            out.append(chr((ord(c) - A - shift) % 26 + A))
        elif "a" <= c <= "z":
            out.append(chr((ord(c) - ord("a") - shift) % 26 + ord("a")))
        else:
            out.append(c)
    return "".join(out)


def crack(ciphertext, top=3):
    letters = clean(ciphertext)
    scores = sorted((chi_squared(letters, s), s) for s in range(26))

    best_score, best_shift = scores[0]
    print(f"Letters analyzed: {len(letters)}")
    print(f"Most likely shift: {best_shift} (key letter: {chr(A + best_shift)})")
    print(f"\nDecrypted text:\n{decrypt(ciphertext, best_shift)}")

    print(f"\nTop {top} candidates:")
    for score, shift in scores[:top]:
        preview = decrypt(ciphertext, shift).replace("\n", " ")[:60]
        print(f"  shift {shift:2d} | score {score:8.1f} | {preview}")
    return best_shift


def read_ciphertext_from_user():
    """Read pasted/typed ciphertext. Finish with an empty line (Enter twice)."""
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
        with open(sys.argv[1], encoding="utf-8") as f:
            ciphertext = f.read()
    else:
        ciphertext = read_ciphertext_from_user()

    if not clean(ciphertext):
        print("No ciphertext was received.")
        sys.exit(1)
    print()
    crack(ciphertext)