"""Homework 3 - Vigenere and Kasiski.

Copy this file to  students/studentXX/hw3/solution.py  and fill in the functions.
Keep the function names and parameters exactly as they are: the unit tests call them.
All texts are uppercase A-Z only, with no spaces.
"""
from pathlib import Path


def load_ciphertext(path=None):
    """Read hw3.txt and return the ciphertext as one string of letters. (Ready - do not change.)"""
    path = Path(path) if path else Path(__file__).with_name("hw3.txt")
    lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines()]
    return "".join(l for l in lines if l and not l.startswith("#"))


def encrypt(plaintext: str, key: str) -> str:
    """Vigenere encryption.  encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR" """
    raise NotImplementedError


def decrypt(ciphertext: str, key: str) -> str:
    """The inverse of encrypt."""
    raise NotImplementedError


def find_repeats(ciphertext: str, length: int = 3) -> dict[str, list[int]]:
    """Every sequence of `length` letters that appears at least twice.

    Returns {sequence: [all start positions, ascending, counted from 0]}.
    """
    raise NotImplementedError


def guess_key_length(ciphertext: str, max_length: int = 12) -> int:
    """The most likely key length between 2 and max_length.

    Careful: if the real length is 5, then 10 also divides all the distances.
    Return the shortest length that explains the text.
    """
    raise NotImplementedError


def recover_key(ciphertext: str, key_length: int) -> str:
    """Given the key length, find the key by frequency analysis of each column."""
    raise NotImplementedError


def break_cipher(ciphertext: str) -> tuple[str, str]:
    """Full attack with no hints. Returns (key, plaintext)."""
    raise NotImplementedError


if __name__ == "__main__":
    key, plaintext = break_cipher(load_ciphertext())
    print("key:", key)
    print(plaintext[:200])
