import random


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


def generate_safe_prime(bits=32, iterations=5):
    while True:
        q = random.getrandbits(bits - 1)
        q |= (1 << (bits - 2)) | 1
        is_q_prime, _ = is_prime_miller_rabin(q, iterations)
        if is_q_prime:
            p = 2 * q + 1
            is_p_prime, _ = is_prime_miller_rabin(p, iterations)
            if is_p_prime:
                return p


def generate_primitive_root(prime):
    phi = prime - 1
    while True:
        g = random.randint(2, prime - 1)
        if pow(g, 2, prime) != 1 and pow(g, phi // 2, prime) != 1:
            return g


def diffie_hellman(bit_length=32):
    p = generate_safe_prime(bit_length)
    g = generate_primitive_root(p)
    print(f"Safe prime p: {p}")
    print(f"Primitive root g: {g}")

    a_private_key = random.randint(2, p - 2)
    b_private_key = random.randint(2, p - 2)
    a_public_key = pow(g, a_private_key, p)
    b_public_key = pow(g, b_private_key, p)

    print(f"Alice's private key: {a_private_key}")
    print(f"Alice's public key: {a_public_key}")
    print(f"Bob's private key: {b_private_key}")
    print(f"Bob's public key: {b_public_key}")

    a_shared_secret = pow(b_public_key, a_private_key, p)
    b_shared_secret = pow(a_public_key, b_private_key, p)

    print(f"Alice's shared secret: {a_shared_secret}")
    print(f"Bob's shared secret: {b_shared_secret}")
    assert a_shared_secret == b_shared_secret, "Shared secrets do not match!"
    print("Key exchange successful!")

    return a_shared_secret


shared_secret = diffie_hellman(bit_length=64)
print(f"Shared secret key: {shared_secret}")
