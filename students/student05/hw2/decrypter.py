
from collections import Counter
import matplotlib.pyplot as plt
import string
from pathlib import Path

# ==========================================
# 1. READ CIPHERTEXT
# ==========================================

folder = Path(__file__).resolve().parent

with open(folder / "hw2.txt", "r", encoding="utf-8") as f:
    ciphertext = f.read().upper()

ENGLISH_ORDER = "ETAOINSHRDLUCMFWYPVBGKJQXZ"
ALPHABET = string.ascii_uppercase

# ==========================================
# 2. RECOVERED KEY (MANUAL)
# ==========================================

# OBN happens a lot so its probably "the"
# KEGQ is probably "club" because it comes after "chess"
# XKOXPGR is octopus because it is an animal with 3 hearts
# ZSAHNODK is magnetic because it fits "magnetic field"
# Z and J never apear so i added them to t and y

KEY = {
    "A": "G",
    "B": "H",
    "C": "W",
    "D": "I",
    "E": "L",
    "F": "K",
    "G": "U",
    "H": "N",
    "I": "D",
    "J": "F",
    "K": "C",
    "L": "Y",
    "M": "Q",
    "N": "E",
    "O": "T",
    "P": "P",
    "Q": "B",
    "R": "S",
    "S": "A",
    "T": "J",
    "U": "X",
    "V": "V",
    "W": "R",
    "X": "O",
    "Y": "Z",
    "Z": "M"
}

# Validate the key
# Validate that every letter appearing in the ciphertext has a mapping
cipher_letters = set(c for c in ciphertext if c in ALPHABET)

if not cipher_letters.issubset(KEY):
    missing = cipher_letters - set(KEY)
    raise ValueError(f"Missing mappings: {missing}")

if len(set(KEY.values())) != len(KEY):
    raise ValueError("Two ciphertext letters map to the same plaintext letter.")

# ==========================================
# 3. FREQUENCY ANALYSIS
# ==========================================

def frequency_break(text):
    counts = Counter(
        c for c in text if c in ALPHABET
    )

    ranked_cipher = sorted(
        ALPHABET,
        key=lambda c: (-counts[c], c)
    )

    return {
        ranked_cipher[i]: ENGLISH_ORDER[i]
        for i in range(26)
    }


# ==========================================
# 4. EVALUATE ACCURACY
# ==========================================

def evaluate(guessed, key):
    correct = sum(
        guessed[c] == key[c]
        for c in key
    )

    return correct


# ==========================================
# 5. DECRYPTION
# ==========================================

def decrypt(text, mapping):
    return "".join(
        mapping.get(c, c) if c in ALPHABET else c
        for c in text
    )


# ==========================================
# 6. EXPERIMENT
# ==========================================

lengths = [100, 250, 500, 1000, 2000]
results = []

for n in lengths:

    prefix = ciphertext[:n]

    guessed = frequency_break(prefix)

    print(f"\n{'=' * 40}")
    print(f"First {n} characters")
    print(f"{'=' * 40}")

    if len(KEY) > 0:
        correct = evaluate(guessed, KEY)
        results.append(correct)

        print(f"Correct mappings: {correct}/26")
        print(f"Accuracy: {correct / 26 * 100:.2f}%")
    else:
        print("Fill in KEY to calculate accuracy.")

    print("Frequency mapping:")

    for c in ALPHABET:
        print(f"{c} -> {guessed[c]}", end=" | ")

    print()


# ==========================================
# 7. FULL DECRYPTION
# ==========================================

if len(KEY) == 26:
    print("\n" + "=" * 40)
    print("DECRYPTED TEXT")
    print("=" * 40)

    decrypted = decrypt(ciphertext, KEY)
    print(decrypted)

    # Save decrypted text
    with open(folder / "decrypted.txt", "w", encoding="utf-8") as f:
        f.write(decrypted)


# ==========================================
# 8. GRAPH
# ==========================================

if len(results) == len(lengths):

    plt.figure(figsize=(9, 5))

    plt.plot(
        lengths,
        results,
        marker="o"
    )

    plt.xlabel("Ciphertext length (characters)")
    plt.ylabel("Correct letter mappings (out of 24)")
    plt.title("Frequency Analysis Accuracy")

    plt.xticks(lengths)
    plt.yticks(range(0, 25, 2))
    plt.ylim(0, 24)

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        folder / "frequency_analysis.png",
        dpi=300
    )

    plt.show()

# ==========================================
# 9. THREE HARDEST LETTERS
# ==========================================

if len(KEY) == 26:

    errors = Counter()

    for n in lengths:
        guessed = frequency_break(ciphertext[:n])

        for c in ALPHABET:
            if guessed[c] != KEY[c]:
                errors[c] += 1

    hardest = errors.most_common(3)

    print("\nTHREE HARDEST LETTERS")

    for c, mistakes in hardest:
        print(
            f"Ciphertext {c} -> {KEY[c]} | "
            f"Incorrect in {mistakes}/{len(lengths)} experiments"
        )
