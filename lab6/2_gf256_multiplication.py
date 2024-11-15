def gf_mul(a, b):
    p = 0
    for i in range(8):
        if b & 1:
            p ^= a
        carry = a & 0x80
        a <<= 1
        if carry:
            a ^= 0x1B
        a &= 0xFF
        b >>= 1
    return p


# Тестування
a = 0x57
b = 0x83
result = gf_mul(a, b)
print(f"{a:02X} * {b:02X} = {result:02X}")
