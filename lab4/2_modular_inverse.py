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


a = 5
n = 18
inverse = inverse_element(a, n)

if inverse is None:
    print(f"Оберненого елемента для {a} по модулю {n} не існує.")
else:
    print(
        f"Мультиплікативний обернений елемент для {a} по модулю {n}: {inverse}")
