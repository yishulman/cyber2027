"""Unit tests for homework 3 (Vigenere + Kasiski).

Run from the repository root:
    pytest tests/hw3 --student student05

The tests are ordered from easy to hard. Fix them from the top down.
"""
import hashlib
import random
import string

import pytest

ABC = string.ascii_uppercase

# The ciphertext we broke together in class (lesson 3 slides). Key: LEMON.
CLASS_CIPHERTEXT = (
    "ELQGRNVQHBQXTSPTTTSETWFVRVIKOAOXTSXPCYIFEFQYRAXRFBXXTSRYIYMJ"
    "SIZHUPWMARVIKWFFWQRNREUBNYHMUNTRFVRAEFHRCRATGSIWSLLTBSNCWUBG"
    "SIYSFDESSNYHFVRPRQALNEZARLWGFRELQRVDXMBPPFQHJPIZHUPVQDRLXQRC"
    "TIOSFELQZRYKFVBQXTSXPCUGGSIZFRGIMZROEZRGSIDSFESRHUPWQQEPXROY"
    "WWMDNCXQJRCCXSGEIDCSELQARDWMURHEEABGIPPLZRQZREXQFBQXTSXPC"
)


def reference_encrypt(text, key):
    return "".join(ABC[(ABC.index(c) + ABC.index(key[i % len(key)])) % 26] for i, c in enumerate(text))


def random_key(rng, length):
    """A random key. Up to 26 letters the letters are all different, so no shorter key hides inside it."""
    if length <= 26:
        return "".join(rng.sample(ABC, length))
    return "".join(rng.choice(ABC) for _ in range(length))


# ---------- level 1: the cipher itself ----------

def test_encrypt_class_example(sol):
    assert sol.encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"


def test_decrypt_class_example(sol):
    assert sol.decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"


def test_key_a_changes_nothing(sol):
    assert sol.encrypt("HELLOWORLD", "A") == "HELLOWORLD"


def test_one_letter_key_is_caesar(sol):
    assert sol.encrypt("ABCXYZ", "D") == "DEFABC"


def test_key_longer_than_message(sol):
    assert sol.encrypt("HI", "LEMON") == "SM"


def test_round_trip_random_keys(sol, sample_text):
    rng = random.Random(2027)
    for length in (1, 3, 7, 20, 100):
        key = random_key(rng, length)
        assert sol.encrypt(sample_text, key) == reference_encrypt(sample_text, key)
        assert sol.decrypt(sol.encrypt(sample_text, key), key) == sample_text


# ---------- level 2: Kasiski ----------

def test_find_repeats_small(sol):
    assert sol.find_repeats("ABCXXABCYYABC", 3) == {"ABC": [0, 5, 10]}


def test_find_repeats_class_text(sol):
    repeats = sol.find_repeats(CLASS_CIPHERTEXT, 6)
    assert repeats.get("XTSXPC") == [31, 196, 291]
    assert all(len(seq) == 6 and len(pos) >= 2 for seq, pos in repeats.items())


def test_key_length_class_text(sol):
    assert sol.guess_key_length(CLASS_CIPHERTEXT) == 5


@pytest.mark.parametrize("length", [4, 6, 7, 9])
def test_key_length_new_texts(sol, sample_text, length):
    key = random_key(random.Random(100 + length), length)
    assert sol.guess_key_length(reference_encrypt(sample_text, key)) == length


# ---------- level 3: recovering the key ----------

def test_recover_key_class_text(sol):
    assert sol.recover_key(CLASS_CIPHERTEXT, 5) == "LEMON"


@pytest.mark.parametrize("length", [5, 8])
def test_recover_key_new_texts(sol, sample_text, length):
    key = random_key(random.Random(200 + length), length)
    assert sol.recover_key(reference_encrypt(sample_text, key), length) == key


def test_break_cipher_new_text(sol, sample_text):
    """A text you have never seen, so a hard-coded answer will not pass."""
    key = random_key(random.Random(), random.choice([5, 6, 7, 8, 9]))
    found_key, found_plain = sol.break_cipher(reference_encrypt(sample_text, key))
    assert found_key == key
    assert found_plain == sample_text


# ---------- level 4: your personal ciphertext ----------

def test_my_ciphertext_is_untouched(my_ciphertext, expected):
    assert len(my_ciphertext) == expected["length"], "hw3.txt was changed - restore the original file"


def test_break_my_ciphertext(sol, student, my_ciphertext, expected):
    key, plaintext = sol.break_cipher(my_ciphertext)
    assert key.isalpha() and key.isupper() and 5 <= len(key) <= 9
    assert reference_encrypt(plaintext, key) == my_ciphertext, "key and plaintext do not match the ciphertext"
    digest = hashlib.sha256(f"{student}:{plaintext}".encode()).hexdigest()
    assert digest == expected["sha256"], "this is not the original message"


# ---------- level 5: the written part ----------

def test_answers_file_exists(hw_dir):
    answers = hw_dir / "answers.md"
    assert answers.exists(), "missing answers.md"
    assert len(answers.read_text(encoding="utf-8").split()) >= 150, "answers.md is too short for four 'why' questions"


def test_experiment_graph_exists(hw_dir):
    assert list(hw_dir.glob("*.png")), "missing the experiment graph (a .png file)"
