"""Hanukkah challenge - the entangled dreidels.

Copy this file to  students/studentXX/hanukkah/solution.py  and fill in the functions.
Keep the function names and parameters exactly as they are: the unit tests call them.
Texts are Hebrew letters only (22 letters), no spaces; final letters are written as regular letters.
"""
from pathlib import Path

ALPHABET = "אבגדהוזחטיכלמנסעפצקרשת"          # shift of each letter = its index (א=0 ... ת=21)
FINALS = str.maketrans("ךםןףץ", "כמנפצ")
DREIDELS = {"ש": "נגהש", "פ": "נגהפ"}          # the diaspora dreidel and the Land-of-Israel dreidel
SPINS = range(4, 9)                            # the number of spins is hidden: 4 to 8
HERE = Path(__file__).resolve().parent
STORIES = HERE.parents[2] / "assignments" / "hw-hanukkah" / "stories.md"   # a Hebrew corpus you may use


def normalize(text: str) -> str:
    """Keep Hebrew letters only and turn final letters into regular ones. (Ready - do not change.)"""
    return "".join(c for c in text.translate(FINALS) if c in ALPHABET)


def load_letter(path=None) -> str:
    """Read letter.txt and return the ciphertext as one string. (Ready - do not change.)"""
    path = Path(path) if path else HERE / "letter.txt"
    lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines()]
    return normalize("".join(l for l in lines if l and not l.startswith("#")))


def encrypt(plaintext: str, primer: str) -> str:
    """Dreidel autokey: the key is the primer (the 6 dreidel letters) followed by the plaintext itself."""
    raise NotImplementedError


def decrypt(ciphertext: str, primer: str) -> str:
    """The inverse of encrypt. Careful: every letter you decrypt becomes part of the key."""
    raise NotImplementedError


def candidate_primers(dreidel_letters: str, spins: int) -> list[str]:
    """Every primer that `spins` spins of a dreidel with these 4 letters can produce."""
    raise NotImplementedError


def hebrew_score(text: str) -> float:
    """Higher = looks more like Hebrew. Your choice how: letters, pairs of letters, words..."""
    raise NotImplementedError


def break_letter(ciphertext: str) -> tuple[str, str, str]:
    """Full attack with no hints.

    You do not know the dreidel, and you do not know how many times it was spun (4 to 8).
    Returns (dreidel, primer, plaintext), where dreidel is "ש" or "פ":
    the 4th letter of the dreidel that the brothers used, and len(primer) is the number of spins.
    """
    raise NotImplementedError


if __name__ == "__main__":
    dreidel, primer, plaintext = break_letter(load_letter())
    print("dreidel:", dreidel, " spins:", len(primer), primer)
    print(plaintext)
