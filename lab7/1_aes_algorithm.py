# функції з лабораторної роботи №6
def mul02(byte):
    byte = byte & 0xFF
    if (byte & 0x80):
        result = ((byte << 1) ^ 0x1B) & 0xFF
    else:
        result = (byte << 1) & 0xFF
    return result


def mul03(byte):
    return mul02(byte) ^ byte


def gf_mul(a, b):
    p = 0
    a &= 0xFF
    b &= 0xFF
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


def gf_pow(base, exponent):
    result = 1
    current = base
    e = exponent
    while e > 0:
        if e & 1:
            result = gf_mul(result, current)
        current = gf_mul(current, current)
        e >>= 1
    return result & 0xFF


def gf_inv(x):
    if x == 0:
        return 0
    return gf_pow(x, 254)


def rotl_byte(x, n=1):
    n = n % 8
    return ((x << n) & 0xFF) | (x >> (8 - n))


# нелінійне перетворення з використанням математичних операцій
def transform(b):
    r = b
    for shift_count in range(1, 5):
        r ^= rotl_byte(b, shift_count)
    return r ^ 0x63


def transform_inv(b):
    for a in range(256):
        if transform(a) == b:
            return a
    return 0


def sub_byte_value(x):
    inv = gf_inv(x)
    return transform(inv)


def inv_sub_byte_value(x):
    t_inv = transform_inv(x)
    return gf_inv(t_inv)


def create_key_schedule(base_key):
    rcon_values = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
    key_blocks = [base_key[i:i + 4] for i in range(0, len(base_key), 4)]

    for i in range(4, 44):
        temp_block = list(key_blocks[i - 1])
        if i % 4 == 0:
            # RotWord
            temp_block = [temp_block[1], temp_block[2],
                          temp_block[3], temp_block[0]]
            # SubWord
            temp_block = [sub_byte_value(b) for b in temp_block]
            # XOR з Rcon
            temp_block[0] ^= rcon_values[(i // 4) - 1]
        # XOR із блоком i-4
        key_blocks.append(
            [x ^ y for x, y in zip(key_blocks[i - 4], temp_block)])

    return key_blocks


def xor_state_with_key(state, key_block):
    for row in range(4):
        for col in range(4):
            state[row][col] ^= key_block[row][col]
    return state


def substitute_state_bytes(state):
    for row in range(4):
        for col in range(4):
            state[row][col] = sub_byte_value(state[row][col])
    return state


def shift_state_rows(state):
    for row in range(1, 4):
        shifted = [state[col][row] for col in range(len(state))]
        shifted = shifted[row:] + shifted[:row]
        for col in range(len(state)):
            state[col][row] = shifted[col]
    return state


def mix_state_columns(state):
    for col in range(4):
        a, b, c, d = state[col]
        state[col][0] = mul02(a) ^ mul03(b) ^ c ^ d
        state[col][1] = a ^ mul02(b) ^ mul03(c) ^ d
        state[col][2] = a ^ b ^ mul02(c) ^ mul03(d)
        state[col][3] = mul03(a) ^ b ^ c ^ mul02(d)
    return state


def aes_encrypt(input_block, key):
    state = [[0] * 4 for _ in range(4)]
    for row in range(4):
        for col in range(4):
            state[row][col] = input_block[row * 4 + col]

    print("\nПочатковий блок:")
    display_state(state)

    key_state = [[0] * 4 for _ in range(4)]
    for row in range(4):
        for col in range(4):
            key_state[row][col] = key[row * 4 + col]

    print("Ключ:")
    display_state(key_state)

    key_schedule = create_key_schedule(key)
    state = xor_state_with_key(state, key_schedule[0:4])
    print()

    for round in range(1, 10):
        state = substitute_state_bytes(state)
        state = shift_state_rows(state)
        state = mix_state_columns(state)
        state = xor_state_with_key(
            state, key_schedule[round * 4: (round + 1) * 4])

        print(f"Після round {round}:")
        display_state(state)

    state = substitute_state_bytes(state)
    state = shift_state_rows(state)
    state = xor_state_with_key(state, key_schedule[40:])

    print("Кінцевий стан:")
    display_state(state)

    encrypted_block = [state[row][col] for row in range(4) for col in range(4)]
    return bytes(encrypted_block)


def unshift_rows(state):
    for row in range(1, 4):
        shifted = [state[col][row] for col in range(len(state))]
        shifted = shifted[-row:] + shifted[:-row]
        for col in range(len(state)):
            state[col][row] = shifted[col]
    return state


def inverse_substitute_bytes(state):
    for row in range(4):
        for col in range(4):
            state[row][col] = inv_sub_byte_value(state[row][col])
    return state


def unmix_columns(state):
    for col in range(4):
        a, b, c, d = state[col]
        state[col][0] = multiply_by_0e(a) ^ multiply_by_0b(
            b) ^ multiply_by_0d(c) ^ multiply_by_09(d)
        state[col][1] = multiply_by_09(a) ^ multiply_by_0e(
            b) ^ multiply_by_0b(c) ^ multiply_by_0d(d)
        state[col][2] = multiply_by_0d(a) ^ multiply_by_09(
            b) ^ multiply_by_0e(c) ^ multiply_by_0b(d)
        state[col][3] = multiply_by_0b(a) ^ multiply_by_0d(
            b) ^ multiply_by_09(c) ^ multiply_by_0e(d)
    return state


def multiply_by_09(value):
    temp = mul02(value)
    temp = mul02(temp)
    temp = mul02(temp)
    return temp ^ value


def multiply_by_0b(value):
    temp = mul02(value)
    temp = mul02(temp)
    temp ^= value
    temp = mul02(temp)
    return temp ^ value


def multiply_by_0d(value):
    temp = mul02(value)
    temp ^= value
    temp = mul02(temp)
    temp = mul02(temp)
    return temp ^ value


def multiply_by_0e(value):
    temp = mul02(value)
    temp ^= value
    temp = mul02(temp)
    temp ^= value
    temp = mul02(temp)
    return temp


def aes_decrypt(cipher_block, key):
    state = [[0] * 4 for _ in range(4)]
    for row in range(4):
        for col in range(4):
            state[row][col] = cipher_block[row * 4 + col]

    key_schedule = create_key_schedule(key)
    state = xor_state_with_key(state, key_schedule[40:])

    for round in range(9, 0, -1):
        state = unshift_rows(state)
        state = inverse_substitute_bytes(state)
        state = xor_state_with_key(
            state, key_schedule[round * 4: (round + 1) * 4])
        state = unmix_columns(state)

        print(f"Після round {round + 1}:")
        display_state(state)

    state = unshift_rows(state)
    state = inverse_substitute_bytes(state)
    state = xor_state_with_key(state, key_schedule[0:4])

    print("Розшифрований блок:")
    display_state(state)

    decrypted_block = [state[row][col] for row in range(4) for col in range(4)]
    return bytes(decrypted_block)


def display_state(state):
    for row in state:
        print(''.join([hex(byte)[2:].zfill(2) for byte in row]), end=' ')
    print()


message_input = input(
    "Введіть повідомлення довжиною 16 символів: ").encode('utf-8')
key_input = input("Введіть ключ довжиною 16 символів: ")

if len(key_input) != 16:
    print("Ключ має бути 16 символів!")
elif len(message_input) != 16:
    print("Повідомлення має бути 16 символів!")
else:
    key_input = key_input.encode('utf-8')
    encrypted_data = aes_encrypt(message_input, key_input)
    print("\nЗашифровано:")
    print(encrypted_data.hex(), "\n")
    decrypted_data = aes_decrypt(encrypted_data, key_input)
    print("\nРозшифровано:")
    print(decrypted_data.decode('utf-8'))
