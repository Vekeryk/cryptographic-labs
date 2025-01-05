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

def add_elliptic_points(point1, point2, a_coeff, mod_p):
    if point1 == (None, None):
        return point2
    if point2 == (None, None):
        return point1

    if point1[0] == point2[0] and point1[1] != point2[1]:
        return (None, None)

    if point1 == point2:
        inv = modular_inverse(2 * point1[1], mod_p)
        gradient = (3 * point1[0]**2 + a_coeff) * inv % mod_p
    else:
        inv = modular_inverse(point2[0] - point1[0], mod_p)
        gradient = (point2[1] - point1[1]) * inv % mod_p

    x_result = (gradient**2 - point1[0] - point2[0]) % mod_p
    y_result = (gradient * (point1[0] - x_result) - point1[1]) % mod_p

    return (x_result, y_result)

def scalar_multiply(base, scalar, a_coeff, mod_p):
    result = (None, None)
    current = base

    for bit in bin(scalar)[2:]:
        if bit == '1':
            result = add_elliptic_points(result, current, a_coeff, mod_p)
        current = add_elliptic_points(current, current, a_coeff, mod_p)

    return result

def calculate_point_order(start_point, a_coeff, mod_p):
    order = 1
    current = start_point
    print(f"Точка {order}: {current}")
    while current != (None, None):
        current = add_elliptic_points(current, start_point, a_coeff, mod_p)
        order += 1
        print(f"Точка {order}: {current}")
    return order

a = 1
b = 1
prime_modulus = 23
test_point = (17, 20)

if (test_point[1]**2) % prime_modulus == (test_point[0]**3 + a * test_point[0] + b) % prime_modulus:
    point_order = calculate_point_order(test_point, a, prime_modulus)
    print(f"Порядок точки {test_point} для кривої y^2 = x^3 + {a}x + {b} (mod {prime_modulus}): {point_order}")
else:
    print("Точка не належить даній епілептичній кривій!")