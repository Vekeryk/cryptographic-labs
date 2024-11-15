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


p = int(input("Введіть непарне число p > 3 для перевірки на простоту: "))
k = int(input("Введіть кількість раундів k: "))
is_prime, probability = is_prime_miller_rabin(p, k)
if is_prime:
    print(f"Число {p} є ймовірно простим з ймовірністю {probability:.8f}")
else:
    print(f"Число {p} є складеним")
