"""Unit tests for the Hanukkah challenge (dreidel autokey).

Run from the repository root:
    pytest tests/hanukkah --student student05

The tests go from easy to hard. Fix them from the top down.
"""
import hashlib
import random

import pytest

ALPHABET = "אבגדהוזחטיכלמנסעפצקרשת"
DREIDELS = {"ש": "נגהש", "פ": "נגהפ"}


def reference_encrypt(plaintext, primer):
    key = primer + plaintext
    return "".join(ALPHABET[(ALPHABET.index(c) + ALPHABET.index(key[i])) % 22] for i, c in enumerate(plaintext))


def random_primer(rng, dreidel, spins=None):
    """4-8 spins that include the dreidel's 4th letter at least once, so the dreidel can be told."""
    spins = spins or rng.randint(4, 8)
    while True:
        primer = "".join(rng.choice(DREIDELS[dreidel]) for _ in range(spins))
        if dreidel in primer:
            return primer


# ---------- level 1: the cipher ----------

def test_normalize_finals(sol):
    assert sol.normalize("יונתן אחי!") == "יונתנאחי"


def test_encrypt_example(sol):
    assert sol.encrypt("יונתנאחי", "פנגפהנ") == "דקעעצנפס"


def test_first_letters_use_the_primer(sol):
    # with primer אאא... the first 6 letters stay as they are
    assert sol.encrypt("אבגדהו", "אאאאאא") == "אבגדהו"


def test_key_continues_with_the_plaintext(sol):
    # letter 7 (א) is shifted by letter 1 of the plaintext (ב = 1)
    assert sol.encrypt("בבבבבבא", "אאאאאא")[6] == "ב"


def test_round_trip(sol, sample):
    rng = random.Random(25)
    for _ in range(5):
        primer = random_primer(rng, rng.choice("שפ"))
        assert sol.encrypt(sample, primer) == reference_encrypt(sample, primer)
        assert sol.decrypt(sol.encrypt(sample, primer), primer) == sample


# ---------- level 2: the key space ----------

@pytest.mark.parametrize("spins,count", [(4, 256), (6, 4096), (8, 65536)])
def test_candidate_primers_count(sol, spins, count):
    primers = sol.candidate_primers("נגהפ", spins)
    assert len(set(primers)) == count
    assert all(len(p) == spins and set(p) <= set("נגהפ") for p in primers)


def test_hebrew_score_prefers_hebrew(sol, sample):
    scrambled = "".join(random.Random(1).sample(sample, len(sample)))
    assert sol.hebrew_score(sample) > sol.hebrew_score(scrambled)


# ---------- level 3: breaking ----------

@pytest.mark.parametrize("dreidel", ["ש", "פ"])
def test_break_new_letter(sol, sample, dreidel):
    """A letter you have never seen, with a random number of random spins, so a hard-coded answer will not pass."""
    primer = random_primer(random.Random(), dreidel)
    found_dreidel, found_primer, found_plain = sol.break_letter(reference_encrypt(sample, primer))
    assert found_plain == sample
    assert found_primer == primer, f"expected {len(primer)} spins"
    assert found_dreidel == dreidel


# ---------- level 4: your personal letter ----------

def test_break_my_letter(sol, student, hw_dir, expected):
    ciphertext = sol.load_letter(hw_dir / "letter.txt")
    assert len(ciphertext) == expected["length"], "letter.txt was changed - restore the original file"
    dreidel, primer, plaintext = sol.break_letter(ciphertext)
    assert reference_encrypt(plaintext, primer) == ciphertext, "spins and plaintext do not match the letter"
    assert hashlib.sha256(f"{student}:{plaintext}".encode()).hexdigest() == expected["sha256_plain"], "not the original letter"
    assert hashlib.sha256(f"{student}:{dreidel}".encode()).hexdigest() == expected["sha256_dreidel"], "wrong dreidel"


# ---------- level 5: the written part ----------

def test_answers_file(hw_dir):
    answers = hw_dir / "answers.md"
    assert answers.exists(), "missing answers.md"
    assert len(answers.read_text(encoding="utf-8").split()) >= 150, "answers.md is too short"
