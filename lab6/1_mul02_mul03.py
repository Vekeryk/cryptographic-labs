def mul02(byte):
    byte = byte & 0xFF
    if (byte & 0x80):
        result = ((byte << 1) ^ 0x1B) & 0xFF
    else:
        result = (byte << 1) & 0xFF
    return result


def mul03(byte):
    return mul02(byte) ^ byte


# Приклад 1:
byte = 0xD4
result = mul02(byte)
print(f"D4 * 02 = {result:02X}")

# Приклад 2:
byte = 0xBF
result = mul03(byte)
print(f"BF * 03 = {result:02X}")
