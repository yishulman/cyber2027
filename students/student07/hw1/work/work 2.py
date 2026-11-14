ciphertext = "TEOEC LMEELAIUE  AORD  YTOGOHORDHAN HTAI RONFLCHALAO LE HR RERREM M HSNA NDFTOA LTSTAAIENBE MI  TAIETUFAG I NLS  SHKRN IE S VTWHTN  TT  DCSDFMBCEEEL MNFTTAE"

with open("words") as file:
    known_words = {line.strip().lower() for line in file if line.strip()}


def english_score(text):
    sentence_words = text.lower().split()
    count = 0

    for word in sentence_words:
        if word in known_words:
            count += 1

    return count


best_score = -1
best_key = None
best_text = ""
keys_tried = 0
n = len(ciphertext)

for columns in range(2, n + 1):
    keys_tried += 1

    letters = [""] * n
    pos = 0

    for col in range(columns):
        size = len(range(col, n, columns))
        letters[col::columns] = ciphertext[pos:pos + size]
        pos += size

    current_try = "".join(letters)
    score = english_score(current_try)

    if score > best_score:
        best_score = score
        best_key = columns
        best_text = current_try

print("Best key:", best_key)
print("Best score:", best_score)
print("Best text:", best_text)
print("keys_tried:", keys_tried)
