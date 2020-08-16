import math, pyperclip

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def encrypt(key, message):
    return translate(key, message, 'encrypt')
def decrypt(key, message):
    return translate(key, message, 'decrypt')
def translate(key, message, mode):
    translated = [] # stores the encrypted/decrypted message string
    keyIndex = 0
    key = key.upper()

    for symbol in message:
        num = LETTERS.find(symbol.upper())
        if num != -1:
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex])
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex])
            num %= len(LETTERS)

            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())
                keyIndex += 1

            if keyIndex == len(key):
                keyIndex = 0
        else:
            translated.append(symbol)
    return ''.join(translated)
