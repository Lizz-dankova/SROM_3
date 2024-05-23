import time


def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time


def addition(poly_1, poly_2):
    poly_1 = poly_1.zfill(233)
    poly_2 = poly_2.zfill(233)
    c = ['0']
    for i in range(233):
        c.append(str(((int(poly_1[i]) if i < len(poly_1) else 0) ^ (int(poly_2[i]) if i < len(poly_2) else 0))))
    result = ''.join(c)
    return result.lstrip('0') if len(result) <= 233 else result[(len(result) - 233):]


def matrix_create():
    generator_poly = 0b100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010010010001
    multiplicative_matrix = [[0] * 233 for _ in range(233)]
    for i in range(233):
        multiplicative_matrix[i][i] = 1  # Identity for simplicity

    # Add generator to the matrix
    for i in range(1, 233):
        multiplicative_matrix[0][i] = (generator_poly >> (233 - i - 1)) & 1
    return multiplicative_matrix


def left_shift(number, shift):
    num_list = list(number)
    num_list = num_list[shift:] + num_list[:shift]
    result = ''.join(num_list)
    return result


def mul(a, b):
    result = ''
    multiplicative_matrix = matrix_create()

    a = a.zfill(233)
    b = b.zfill(233)

    for z in range(233):
        result_1 = [0 for _ in range(233)]
        result_2 = 0
        pre_1 = left_shift(a, z)
        pre_2 = left_shift(b, z)

        for i in range(233):
            for j in range(233):
                result_1[i] += int(pre_1[j]) * multiplicative_matrix[j][i]
            result_1[i] = result_1[i] % 2

        for i in range(233):
            result_2 += result_1[i] * int(pre_2[i])
        result_2 = result_2 % 2
        result += str(result_2)

    return result.zfill(233)


def square(bitstring):
    shift = 1
    length = len(bitstring)
    shift %= length
    shifted_bits = bitstring[-shift:] + bitstring[:-shift]
    return shifted_bits


def power(poly_1, poly_3):
    result = '1'.zfill(233)
    binary_exponent = ''.join(map(str, poly_3))
    current_power = poly_1
    for bit in binary_exponent[::-1]:
        if bit == '1':
            result = mul(result, current_power)
        current_power = square(current_power)
    return result

def mod_polynomial(dividend, divisor):
    dividend = list(map(int, dividend))
    divisor = list(map(int, divisor))
    while len(dividend) >= len(divisor):
        if dividend[0] == 1:
            for i in range(len(divisor)):
                dividend[i] ^= divisor[i]
        dividend.pop(0)
    return ''.join(map(str, dividend)).lstrip('0') or '0'

def extended_gcd(a, b):
    if b == '0':
        return a, '1', '0'
    else:
        gcd, x1, y1 = extended_gcd(b, mod_polynomial(a, b))
        x = y1
        y = addition(x1, mul(y1, mod_polynomial(a, b)))
        return gcd, x, y

def reverse(poly, mod):
    poly = poly.lstrip('0') or '0'
    gcd, inv, _ = extended_gcd(mod, poly)
    return inv.zfill(233)
    return result


def trace(poly):
    result = 0
    for char in poly:
        result += int(char)
    return result % 2


poly1_str = "110101110"
poly2_str = "101001000"
poly3_str = '100001101'
mod_str = '10000000011'
add_result, add_time = measure_time(addition, poly1_str, poly2_str)
print(f'Addition:  {add_result}')
print(f'Time taken for Addition: {add_time} seconds')

mul_result, mul_time = measure_time(mul, poly1_str, poly2_str)
print(f'Multiply:  {mul_result}')
print(f'Time taken for Multiply: {mul_time} seconds')

sq_result, sq_time = measure_time(square, poly1_str)
print(f'Square:  {sq_result}')
print(f'Time taken for Square: {sq_time} seconds')

reverse_result, reverse_time = measure_time(reverse, poly1_str, mod_str)
print(f'Reverse:  {reverse_result}')
print(f'Time taken for Reverse: {reverse_time} seconds')

pow_result, pow_time = measure_time(power, poly1_str, poly3_str)
print(f'Power:  {pow_result}')
print(f'Time taken for Power: {pow_time} seconds')
