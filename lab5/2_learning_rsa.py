import random


def is_prime_miller_rabin(p, k=40):
    if p == 2:
        return True, 1.0
    if p <= 1 or p % 2 == 0:
        return False, 0.0

    d = p - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randrange(2, p - 1)
        x = pow(a, d, p)
        if x == 1 or x == p - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, p)
            if x == p - 1:
                break
        else:
            return False, 0.0

    probability = 1 - (1 / 4) ** k
    return True, probability


def gcdex(a, b):
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def inverse_element(a, n):
    d, x, _ = gcdex(a, n)
    if d != 1:
        return None
    return x % n


def generate_random_prime(bits=1024):
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1))
        candidate |= 1
        prime, _ = is_prime_miller_rabin(candidate, k=40)
        if prime:
            return candidate


def generate_keys(bits=1024):
    p = generate_random_prime(bits)
    q = generate_random_prime(bits)
    while q == p:
        q = generate_random_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Зазвичай беруть e = 65537
    e = 65537
    d = inverse_element(e, phi)
    if d is None:
        for candidate in range(3, 100000, 2):
            if gcdex(candidate, phi)[0] == 1:
                e = candidate
                d = inverse_element(e, phi)
                if d is not None:
                    break

    return (e, n), (d, n)


if __name__ == "__main__":
    print("Генеруємо ключі для RSA...")
    public_key, private_key = generate_keys(bits=1024)
    e, n = public_key
    d, n = private_key
    print(f"Публічний ключ: (e={e})")
    print(f"Приватний ключ: (d={d})")

    letter_to_num = {
        'А': 0, 'Б': 1, 'В': 2, 'Г': 3, 'Ґ': 4, 'Д': 5, 'Е': 6, 'Є': 7, 'Ж': 8, 'З': 9,
        'И': 10, 'І': 11, 'Ї': 12, 'Й': 13, 'К': 14, 'Л': 15, 'М': 16, 'Н': 17, 'О': 18,
        'П': 19, 'Р': 20, 'С': 21, 'Т': 22, 'У': 23, 'Ф': 24, 'Х': 25, 'Ц': 26, 'Ч': 27,
        'Ш': 28, 'Щ': 29, 'Ь': 30, 'Ю': 31, 'Я': 32
    }

    num_to_letter = {v: k for k, v in letter_to_num.items()}
    message = "студент"
    message = message.upper()

    # Перетворюємо слово у числа
    message_numbers = [letter_to_num[ch] for ch in message]
    print("Оригінальне слово:", message)
    print("Числове представлення:", message_numbers)

    # Шифруємо кожну літеру: c = m^e mod n
    encrypted = [pow(m, e, n) for m in message_numbers]

    # Дешифруємо кожну літеру: m = c^d mod n
    decrypted_numbers = [pow(c, d, n) for c in encrypted]
    print("Дешифровані числа:", decrypted_numbers)

    decrypted_message = "".join(num_to_letter[m] for m in decrypted_numbers)
    print("Розшифроване слово:", decrypted_message)
