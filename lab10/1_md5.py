# Константи згідно з RFC 1321
s = [
    7, 12, 17, 22,  # Рунди для операцій F
    5, 9, 14, 20,   # Рунди для операцій G
    4, 11, 16, 23,  # Рунди для операцій H
    6, 10, 15, 21   # Рунди для операцій I
]

K = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
]


def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF


def int_to_little_endian_32bit(val):
    return bytes([
        val & 0xFF,
        (val >> 8) & 0xFF,
        (val >> 16) & 0xFF,
        (val >> 24) & 0xFF
    ])


def int_to_little_endian_64bit(val):
    return bytes([
        val & 0xFF,
        (val >> 8) & 0xFF,
        (val >> 16) & 0xFF,
        (val >> 24) & 0xFF,
        (val >> 32) & 0xFF,
        (val >> 40) & 0xFF,
        (val >> 48) & 0xFF,
        (val >> 56) & 0xFF
    ])


def bytes_to_little_endian_32bit_array(b):
    # Розбиваємо блок по 4 байти та конвертуємо в 32-бітні числа (little-endian)
    arr = []
    for i in range(0, len(b), 4):
        val = (b[i]) | (b[i + 1] << 8) | (b[i + 2] << 16) | (b[i + 3] << 24)
        arr.append(val)
    return arr


def md5(message: bytes) -> str:
    # Початкові значення буферів
    a0 = 0x67452301
    b0 = 0xEFCDAB89
    c0 = 0x98BADCFE
    d0 = 0x10325476

    original_length = len(message) * 8

    # Додаємо 0x80
    message += b'\x80'

    # Доповнюємо нулями, доки довжина (в бітах) % 512 != 448
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'

    # Додаємо довжину повідомлення (64 біти, little-endian)
    message += int_to_little_endian_64bit(original_length)

    # Обробка блоків по 512 біт (64 байти)
    for i in range(0, len(message), 64):
        block = message[i:i + 64]
        M = bytes_to_little_endian_32bit_array(block)

        A, B, C, D = a0, b0, c0, d0

        for j in range(64):
            if 0 <= j <= 15:
                F = (B & C) | ((~B) & D)
                g = j
            elif 16 <= j <= 31:
                F = (D & B) | ((~D) & C)
                g = (5 * j + 1) % 16
            elif 32 <= j <= 47:
                F = B ^ C ^ D
                g = (3 * j + 5) % 16
            else:
                F = C ^ (B | (~D))
                g = (7 * j) % 16

            F = (F + A + K[j] + M[g]) & 0xFFFFFFFF
            A = D
            D = C
            C = B
            B = (B + left_rotate(F, s[(j // 16) * 4 + (j % 4)])) & 0xFFFFFFFF

        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF

    # Формуємо результуючий хеш (128 біт)
    digest = (int_to_little_endian_32bit(a0) +
              int_to_little_endian_32bit(b0) +
              int_to_little_endian_32bit(c0) +
              int_to_little_endian_32bit(d0))

    return ''.join('{:02x}'.format(byte) for byte in digest)


if __name__ == "__main__":
    # Тест 1: "abc"
    test_input = b"abc"
    print("Input:", test_input)
    print("MD5:", md5(test_input))
    print("Expected: 900150983cd24fb0d6963f7d28e17f72")
    print()

    # Тест 2: "hello world"
    test_input = b"hello world"
    print("Input:", test_input)
    print("MD5:", md5(test_input))
    print("Expected: 5eb63bbbe01eeed093cb22bb8f5acdc3")
