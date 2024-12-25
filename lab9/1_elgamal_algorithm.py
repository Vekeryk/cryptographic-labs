import random
from math import gcd


# функція з лабораторної роботи №5
def is_prime_miller_rabin(p, k):
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


# Генерація простого числа
def generate_prime(bits, k):
    while True:
        p = random.getrandbits(bits) | 1
        is_prime, _ = is_prime_miller_rabin(p, k)
        if is_prime:
            return p


# Перевірка первісного кореня
def is_primitive_root(g, p):
    if gcd(g, p) != 1:
        return False

    required_set = set(pow(g, i, p) for i in range(1, p))
    return len(required_set) == p - 1


# Генерація первісного кореня
def find_primitive_root(p):
    for g in range(2, p):
        if is_primitive_root(g, p):
            return g
    return None


# Алгоритм Ель-Гамаля
class ElGamal:
    def __init__(self, p, g):
        self.p = p
        self.g = g
        self.x = random.randint(1, p - 2)  # Приватний ключ
        self.y = pow(g, self.x, p)  # Публічний ключ

    def encrypt(self, m):
        r = random.randint(1, self.p - 2)
        c1 = pow(self.g, r, self.p)
        c2 = (m * pow(self.y, r, self.p)) % self.p
        return c1, c2, r

    def decrypt(self, c1, c2):
        s = pow(c1, self.x, self.p)
        s_inv = pow(s, -1, self.p)
        m = (c2 * s_inv) % self.p
        return m


bits = 16  # Розрядність простого числа
k = 10  # Кількість раундів тесту Рабіна-Міллера

p = generate_prime(bits, k)
g = find_primitive_root(p)

elgamal = ElGamal(p, g)

message = 123  # Повідомлення для шифрування
c1, c2, r = elgamal.encrypt(message)
decrypted_message = elgamal.decrypt(c1, c2)

print(f"(p): {p}")
print(f"(g): {g}")
print(f"Private key (x): {elgamal.x}")
print(f"Public key (y): {elgamal.y}")
print(f"Message (m): {message}")
print(f"Random (r): {r}")
print(f"(c1): {c1} (c2): {c2}")
print(f"Decrypted message: {decrypted_message}")
