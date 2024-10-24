import re


def create_matrix(plaintext, row_key, column_key):
    rows = len(row_key)
    cols = len(column_key)

    # Створюємо порожню матрицю
    matrix = [['' for _ in range(cols)] for _ in range(rows)]

    # Заповнюємо матрицю текстом
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(plaintext):
                # Пропускаємо спецсимволи
                while not plaintext[idx].isalnum():
                    idx += 1

                matrix[r][c] = plaintext[idx]
                idx += 1
            else:
                # Якщо текст коротший за розмір матриці, заповнюємо пробілами
                matrix[r][c] = ' '

    return matrix


def sort_key(key):
    # Створюємо список з індексами символів у відсортованому порядку
    return sorted(range(len(key)), key=lambda x: key[x])


def encrypt(plaintext, row_key, column_key):
    # Створюємо матрицю
    matrix = create_matrix(plaintext, row_key, column_key)
    for row in matrix:
        print(row)
    print()

    # Сортуємо ключі
    sorted_column_indices = sort_key(column_key)
    print(sorted_column_indices)
    sorted_row_indices = sort_key(row_key)
    print(sorted_row_indices)
    print()

    # Формуємо зашифрований текст
    result = []
    for c in sorted_column_indices:
        for r in sorted_row_indices:
            result.append(matrix[r][c])
        result.append(' ')

    return ''.join(result)


def decrypt(ciphertext, row_key, column_key):
    row_amount = len(row_key)
    col_amount = len(column_key)

    # Розбиваємо зашифрований текст на списки по колонках
    pure_ciphertext = []
    index = 0
    for c in ciphertext:
        if index != 0 and index % 4 == 0:
            index = 0
            continue
        pure_ciphertext.append(c)
        index += 1

    print(pure_ciphertext)
    words = re.findall('.' * row_amount, ''.join(pure_ciphertext))
    print(words)

    # Сортуємо ключі
    sorted_column_indices = sort_key(column_key)
    sorted_row_indices = sort_key(row_key)

    # Створюємо порожню матрицю
    matrix = [['' for _ in range(col_amount)] for _ in range(row_amount)]

    # Заповнюємо матрицю зашифрованими даними
    for idx, c in enumerate(sorted_column_indices):
        col_data = words[idx]
        if len(col_data) < len(sorted_row_indices):
            # Якщо стовпець коротший, доповнюємо пробілами
            col_data += ' ' * (len(sorted_row_indices) - len(col_data))
        for r_idx, r in enumerate(sorted_row_indices):
            matrix[r][c] = col_data[r_idx]

    # Відновлюємо початковий текст
    plaintext = []
    for r in range(row_amount):
        for c in range(col_amount):
            plaintext.append(matrix[r][c])

    return ''.join(plaintext).strip()


# Приклад з лекції
plaintext = "програмне забезпечення"
column_key = "крипто"
row_key = "шифр"
print(f"Початковий текст: {plaintext}")

encrypted_text = encrypt(plaintext, row_key, column_key)
print(f"Зашифрований текст: {encrypted_text}")

decrypted_text = decrypt(encrypted_text, row_key, column_key)
print(f"Розшифрований текст: {decrypted_text}")
