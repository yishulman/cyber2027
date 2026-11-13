
import re
import math
import random
import matplotlib.pyplot as plt
from wordfreq import zipf_frequency


# ==========================================
# 1. ENGLISH SCORE
# ==========================================

def english_score(text):
    words = re.findall(r"[a-zA-Z]+", text.lower())

    if not words:
        return 0

    scores = [
        zipf_frequency(word, "en")
        for word in words
    ]

    return sum(scores) / len(scores)


# ==========================================
# 2. CAESAR CIPHER
# ==========================================

def caesar_encrypt(text, key):
    result = ""

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')

            result += chr(
                (ord(char) - base + key) % 26 + base
            )
        else:
            result += char

    return result


def caesar_decrypt(text, key):
    return caesar_encrypt(text, -key)


def crack_caesar(ciphertext):
    candidates = []

    for key in range(26):
        plaintext = caesar_decrypt(ciphertext, key)
        score = english_score(plaintext)

        candidates.append((score, key, plaintext))

    return max(candidates)


# ==========================================
# 3. COLUMNAR TRANSPOSITION CIPHER
# ==========================================

def transposition_encrypt(plaintext, key):
    result = ""

    for col in range(key):
        for i in range(col, len(plaintext), key):
            result += plaintext[i]

    return result


def transposition_decrypt(ciphertext, key):
    num_cols = key
    num_rows = math.ceil(len(ciphertext) / num_cols)

    short_cols = num_cols - (len(ciphertext) % num_cols)

    if len(ciphertext) % num_cols == 0:
        short_cols = 0

    plaintext = [''] * num_rows
    index = 0

    for col in range(num_cols):
        col_length = num_rows - (
            1 if col >= num_cols - short_cols else 0
        )

        for row in range(col_length):
            plaintext[row] += ciphertext[index]
            index += 1

    return ''.join(plaintext)


def crack_transposition(ciphertext):
    candidates = []

    for key in range(2, len(ciphertext) + 1):
        plaintext = transposition_decrypt(ciphertext, key)
        score = english_score(plaintext)

        candidates.append((score, key, plaintext))

    return max(candidates)


# ==========================================
# 4. ORIGINAL ENCRYPTED MESSAGES
# ==========================================

caesar_text = (
    "TY ESP LQEPCYZZY ESP HTYO NSLYRPO "
    "OTCPNETZY LYO ESP NWZFOD XZGPO EZHLCO "
    "ESP DPL HSPY ESP WTRSED HPYE ZFE "
    "ESP NSTWOCPY EZWO"
)

transposition_text = (
    "TT TTS OHAEIEAS TWHTMHO BRORTV TEB REEEU TU OYTEWE ETO EERDHDTL EDE IEONC TSIEGH TR EBTN GOW DS EELH TKE  TMIOACNT IEAHSCHSHMLNYUE SB RR AAEEIL  SWFCRLRELUDN "
)


# ==========================================
# 5. BREAK THE ORIGINAL CIPHERS
# ==========================================

print("=" * 50)
print("CAESAR CIPHER")
print("=" * 50)

score, key, plaintext = crack_caesar(caesar_text)

print("Key:", key)
print("Plaintext:", plaintext)
print("English score:", score)


print("\n" + "=" * 50)
print("TRANSPOSITION CIPHER")
print("=" * 50)

score, key, plaintext = crack_transposition(transposition_text)

print("Key:", key)
print("Plaintext:", plaintext)
print("English score:", score)


# ==========================================
# 6. GENERATE RANDOM ENGLISH TEXT
# ==========================================

words = [
    "the", "house", "cat", "dog", "hello",
    "world", "computer", "school", "happy",
    "today", "good", "morning", "people",
    "student", "learn", "python", "science",
    "beautiful", "language", "message",
    "friend", "book", "water", "music"
]


def generate_english_text(length):
    text = ""

    while len(text) < length:
        text += random.choice(words) + " "

    return text[:length]


# ==========================================
# 7. EXPERIMENT
# ==========================================

lengths = [5, 10, 20, 50, 100]

success_rates = []

random.seed(42)

for length in lengths:

    correct = 0

    for _ in range(30):

        # Generate original English message
        plaintext = generate_english_text(length)

        # Select random Caesar key
        original_key = random.randint(0, 25)

        # Encrypt message
        ciphertext = caesar_encrypt(
            plaintext,
            original_key
        )

        # Attempt to crack automatically
        score, found_key, decrypted = crack_caesar(
            ciphertext
        )

        # Check whether key is correct
        if found_key == original_key:
            correct += 1

    accuracy = (correct / 30) * 100

    success_rates.append(accuracy)

    print(
        f"Length: {length:3} | "
        f"Correct: {correct}/30 | "
        f"Success rate: {accuracy:.2f}%"
    )


# ==========================================
# 8. DRAW GRAPH
# ==========================================

plt.figure(figsize=(9, 5))

plt.plot(
    lengths,
    success_rates,
    marker='o',
    linewidth=2,
    markersize=8
)

plt.xlabel("Text Length (characters)")
plt.ylabel("Success Rate (%)")

plt.title(
    "Caesar Cipher Brute Force Success Rate"
)

plt.xticks(lengths)
plt.yticks(range(0, 101, 10))

plt.ylim(0, 100)

plt.grid(True)

for x, y in zip(lengths, success_rates):
    plt.annotate(
        f"{y:.1f}%",
        (x, y),
        textcoords="offset points",
        xytext=(0, 10),
        ha='center'
    )

plt.tight_layout()

plt.savefig("caesar_results.png")

plt.show()


# ==========================================
# 9. NUMBER OF TRANSPOSITION KEYS
# ==========================================

print("\n" + "=" * 50)
print("TRANSPOSITION KEY COUNTS")
print("=" * 50)

for length in lengths:
    number_of_keys = length - 1

    print(
        f"Message length: {length:3} | "
        f"Keys tested: {number_of_keys}"
    )


print("\nExperiment completed!")
print("Graph saved as caesar_results.png")
