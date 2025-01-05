import random

def gcdex(a, b):
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def modular_inverse(a, modulus):
    gcd, x, _ = gcdex(a, modulus)
    if gcd == 1:
        return x % modulus
    else:
        raise ValueError("Оберненого елемента не існує!")

def find_generator(a, b, p):
    x, y = random.randint(1, p - 1), random.randint(1, p - 1)
    while (y ** 2) % p != (x ** 3 + a * x + b) % p:
        x, y = random.randint(0, p - 1), random.randint(0, p - 1)

    return (x, y)

def add_points(p, q, a, p_mod):
    if p == (None, None):
        return q
    if q == (None, None):
        return p
    if p[0] == q[0] and p[1] != q[1]:
        return (None, None)

    if p == q:
        m = (3 * p[0]**2 + a) * modular_inverse(2 * p[1], p_mod) % p_mod
    else:
        m = (q[1] - p[1]) * modular_inverse(q[0] - p[0], p_mod) % p_mod

    x_r = (m**2 - p[0] - q[0]) % p_mod
    y_r = (m * (p[0] - x_r) - p[1]) % p_mod
    return (x_r, y_r)

def scalar_multiply(point, scalar, a, p_mod):
    result = (None, None)
    current = point
    while scalar:
        if scalar & 1:
            result = add_points(result, current, a, p_mod)
        current = add_points(current, current, a, p_mod)
        scalar >>= 1
    return result

def find_order(base_point, a, p):
    order = 1
    result = base_point
    while result != (None, None):
        result = add_points(result, base_point, a, p)
        order += 1
    return order

def generate_keypair(generator, a, p):
    private_key = random.randint(1, find_order(generator, a, p) - 1)
    public_key = scalar_multiply(generator, private_key, a, p)
    return private_key, public_key

def encrypt(message, public_key, generator, a, p):
    k = random.randint(1, find_order(generator, a, p) - 1)
    c1 = scalar_multiply(generator, k, a, p)
    shared_secret = scalar_multiply(public_key, k, a, p)
    c2 = add_points(message, shared_secret, a, p)
    return c1, c2

def decrypt(c1, c2, private_key, a, p):
    shared_secret = scalar_multiply(c1, private_key, a, p)
    shared_secret_inverse = (shared_secret[0], (-shared_secret[1]) % p)
    plaintext = add_points(c2, shared_secret_inverse, a, p)
    return plaintext

a = 1
b = 1
mod_p = 23
base_point = (17, 20)

private_key, public_key = generate_keypair(base_point, a, mod_p)
print("Закритий ключ:", private_key)
print("Відкритий ключ:", public_key)

message_point = (3, 10)

ciphertext = encrypt(message_point, public_key, base_point, a, mod_p)
print("Шифротекст:", ciphertext)

decrypted_message = decrypt(ciphertext[0], ciphertext[1], private_key, a, mod_p)
print("Розшифроване повідомлення:", decrypted_message)

assert decrypted_message == message_point, "Розшифрування невірне!"