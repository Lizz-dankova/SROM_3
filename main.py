import time

# Генератор поля (x^233 + x^9 + x^4 + x + 1)
mod_polynomial = '100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000010011'

def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

def addition(poly_1, poly_2):
    poly_1 = poly_1.zfill(233)
    poly_2 = poly_2.zfill(233)
    result = ''.join(str(int(a) ^ int(b)) for a, b in zip(poly_1, poly_2))
    return result.lstrip('0') or '0'

def left_shift(number, shift):
    return (number[shift:] + '0' * shift)[:233]

def mod_polynomial_func(dividend, divisor=mod_polynomial):
    divisor_len = len(divisor)
    dividend = list(dividend)
    while len(dividend) >= divisor_len:
        if dividend[0] == '1':
            for i in range(divisor_len):
                dividend[i] = str(int(dividend[i]) ^ int(divisor[i]))
        dividend.pop(0)
    return ''.join(dividend).lstrip('0') or '0'

def mul(a, b):
    a = a.zfill(233)
    b = b.zfill(233)
    result = [0] * (2 * 233)
    for i in range(233):
        if b[232 - i] == '1':
            for j in range(233):
                result[i + j] ^= int(a[232 - j])
    result = ''.join(map(str, result))
    return mod_polynomial_func(result, mod_polynomial)

def square(bitstring):
    interleaved = ''.join(bit + '0' for bit in bitstring[:-1]) + bitstring[-1]
    return mod_polynomial_func(interleaved, mod_polynomial)

def power(poly_1, poly_3):
    result = '1'.zfill(233)
    current_power = poly_1
    for bit in poly_3:
        if bit == '1':
            result = mul(result, current_power)
        current_power = square(current_power)
    return result

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        q, r = divmod(a, b)
        gcd, x1, y1 = extended_gcd(b, r)
        x = y1
        y = x1 - q * y1
        return gcd, x, y

def reverse(poly):
    poly_int = int(poly, 2)
    mod_int = int(mod_polynomial, 2)
    gcd, inv, _ = extended_gcd(mod_int, poly_int)
    if gcd != 1:
        raise ValueError("Inverse does not exist")
    inv_bin = bin(inv)[2:].zfill(233)
    return inv_bin

def trace(poly):
    return str(sum(map(int, poly)) % 2)

poly1 = str(input("Enter the first polynomial: "))
poly2 = str(input("Enter the second polynomial: "))
poly3 = str(input("Enter the third polynomial: "))

add_result, add_time = measure_time(addition, poly1, poly2)
print(f'Addition:  {add_result}')
print(f'Time taken for Addition: {add_time} seconds')

mul_result, mul_time = measure_time(mul, poly1, poly2)
print(f'Multiply:  {mul_result}')
print(f'Time taken for Multiply: {mul_time} seconds')

sq_result, sq_time = measure_time(square, poly1)
print(f'Square:  {sq_result}')
print(f'Time taken for Square: {sq_time} seconds')

try:
    reverse_result, reverse_time = measure_time(reverse, poly1)
    print(f'Reverse:  {reverse_result}')
    print(f'Time taken for Reverse: {reverse_time} seconds')
except ValueError as e:
    print(e)

pow_result, pow_time = measure_time(power, poly1, poly3)
print(f'Power:  {pow_result}')
print(f'Time taken for Power: {pow_time} seconds')
