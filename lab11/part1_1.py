def calculate_curve_points(a, b, p):
    results = []
    for x in range(p):
        y_squared = (x**3 + a * x + b) % p
        for y in range(p):
            if y**2 % p == y_squared:
                results.append((x, y))
    return results

a_param = 1
b_param = 1
prime_modulo = 23
elliptic_curve_points = calculate_curve_points(a_param, b_param, prime_modulo)

print("Точки еліптичної кривої для рівняння y^2 ≡ x^3 + x + 1 (mod 23):")
print(", ".join(str(point) for point in elliptic_curve_points))
