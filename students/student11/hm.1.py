def caesar_decrypt(text, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    for char in text:
        if char in alphabet:
            place = alphabet.index(char)
            new_place = (place - key) % 26
            result += alphabet[new_place]
        else:
            result += char

    return result

def break_caesar(text):
    best_score = -1
    best_key = 0
    best_text = ""

    for key in range(26):
        decoded = caesar_decrypt(text, key)
        score = english_score(decoded)

        if score > best_score:
            best_score = score
            best_key = key
            best_text = decoded

    return best_key, best_text

def english_score(text):
    words = [" THE ", " AND ", " THAT ", " WHO ",
             " HAVE ", " WITH ", " FOR ", " YOU ",
             " SOME ", " MORE ", " EVERY ", " DAY ",
             " FAMILY ", " READ ", " BIRDS "]

    score = 0
    text = " " + text.upper() + " "

    for word in words:
        if word in text:
            score += 1
    return score
