def encrypt(msg: str, width: int) -> str:
    ciphertext = ""

    for col in range(width):
        for i in range(col, len(msg), width):
            ciphertext += msg[i]

    return ciphertext


def decrypt(ciphertext: str, width: int) -> str:
    rows = (len(ciphertext) + width - 1) // width
    extra = len(ciphertext) % width

    if extra == 0:
        extra = width

    columns = []
    index = 0

    for col in range(width):
        col_length = rows if col < extra else rows - 1
        columns.append(ciphertext[index:index + col_length])
        index += col_length

    plaintext = ""

    for row in range(rows):
        for col in range(width):
            if row < len(columns[col]):
                plaintext += columns[col][row]

    return plaintext