alphabet = 'абвгґдежзийіїклмнопрстуфхцчшщьюя'


def get_cipher_alphabet(key, keyword):
    new_start = key + len(keyword)

    first_part = [alphabet[x]
                  for x in range(new_start, len(alphabet)) if alphabet[x] not in keyword]

    second_part = [alphabet[x]
                   for x in range(0, new_start) if alphabet[x] not in keyword]

    cipher_alphabet_array = first_part + list(keyword) + second_part

    # print(first_part, second_part)
    # print(cipher_alphabet_array)
    # print()

    cipher_alphabet = ''.join(cipher_alphabet_array)

    # print(alphabet)
    # print(cipher_alphabet)
    # print()

    return cipher_alphabet


def encrypt(plaintext, key, keyword):
    cipher_alphabet = get_cipher_alphabet(key, keyword)

    result = ''
    for char in plaintext.lower():
        if char in alphabet:
            index = alphabet.index(char)
            result += cipher_alphabet[index]
    return result


def decrypt(ciphertext, key, keyword):
    cipher_alphabet = get_cipher_alphabet(key, keyword)

    result = ''
    for char in ciphertext.lower():
        if char in alphabet:
            index = cipher_alphabet.index(char)
            result += alphabet[index]
    return result


plaintext = "жага до знань"
key = 10
keyword = "праця"

print(f"Початковий текст: {plaintext}, K: {key}, ключове слово: {keyword}")

cipher_alphabet = get_cipher_alphabet(key, keyword)
print(alphabet)
print(cipher_alphabet)

ciphertext = encrypt(plaintext, key, keyword)
print('Зашифрований текст:', ciphertext)

decrypted_text = decrypt(ciphertext, key, keyword)
print('Розшифрований текст:', decrypted_text)
