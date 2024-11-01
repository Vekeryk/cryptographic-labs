def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def phi(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result


def inverse_element_2(a, n):
    if gcd(a, n) != 1:
        return None
    phi_n = phi(n)
    return pow(a, phi_n - 1, n)


a = 5
n = 18
inverse = inverse_element_2(a, n)
if inverse is None:
    print(f"Оберненого елемента для {a} по модулю {n} не існує.")
else:
    print(
        f"Мультиплікативний обернений елемент для {a} по модулю {n}: {inverse}")
