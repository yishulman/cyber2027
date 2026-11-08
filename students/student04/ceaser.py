
import string


def prepare_for_encryption(text:str) -> str:
    return ''.join(
        char for char in text.upper()
        if 'A' <= char <= 'Z'
    )

def decrypt(msg: str, key: int) -> str:
    decrypted = ""
    for letter in msg:
        if letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            decrypted += chr(
                (ord(letter) - ord("A") - key) % 26 + ord("A")
            )
        else:
            decrypted += letter
    return decrypted


def encrypt(msg: str, key: int) -> str:
    encrypted = ""

    for letter in msg:
        if letter.isalpha() and letter.isascii():
            encrypted += chr(
                (ord(letter.upper()) - ord("A") + key) % 26 + ord("A")
            )
        else:
            encrypted += letter

    return encrypted


