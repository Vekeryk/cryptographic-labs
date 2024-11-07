import re
import random

ukrainian_letters = [
    'О', 'А', 'И', 'Е', 'Н', 'І', 'В', 'Т', 'Р', 'С', 'Л', 'К', 'Д',
    'М', 'У', 'З', 'П', 'Я', 'Ь', 'Б', 'Г', 'Ч', 'Й', 'Х', 'Ж', 'Ш',
    'Ю', 'Є', 'Ц', 'Щ', 'Ф', 'Ї', 'Ґ'
]

codes_list = list(range(100, 1000))

# Перемішуємо список кодів
random.shuffle(codes_list)

# Перевірка, що вистачає кодів для всіх літер
if len(codes_list) < len(ukrainian_letters) * 3:
    raise ValueError("Недостатньо кодів для всіх літер.")

# Призначаємо по три коди для кожної літери
letters_to_codes = {}
codes_to_letters = {}

for letter in ukrainian_letters:
    codes = [codes_list.pop() for _ in range(3)]
    letters_to_codes[letter] = codes
    for code in codes:
        codes_to_letters[code] = letter


def encrypt(plaintext):
    ciphertext = []
    for char in plaintext.upper():
        if char in letters_to_codes:
            code = random.choice(letters_to_codes[char])
            ciphertext.append(str(code))

    return ''.join(ciphertext)


def decrypt(ciphertext):
    plaintext = []
    words = ciphertext.split()
    for word in words:
        tokens = re.findall('...', word)
        for token in tokens:
            if token.isdigit():
                code = int(token)
                letter = codes_to_letters.get(code, '?')
                plaintext.append(letter.lower())
            else:
                # Додаємо нечислові токени без змін
                plaintext.append(token)

    return ''.join(plaintext)


# Приклад використання
print(letters_to_codes)

plaintext = 'привіт мій прекрасний світ'
print(f"Початковий текст: {plaintext}")

ciphertext = encrypt(plaintext)
print('Зашифрований текст:', ciphertext)

decrypted_text = decrypt(ciphertext)
print('Розшифрований текст:', decrypted_text)
