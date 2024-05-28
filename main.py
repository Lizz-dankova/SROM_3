import time


def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time


def addition(poly_1, poly_2):
    poly_1 = poly_1.zfill(173)
    poly_2 = poly_2.zfill(173)
    c = ['0']
    for i in range(173):
        c.append(str(((int(poly_1[i]) if i < len(poly_1) else 0) + (int(poly_2[i]) if i < len(poly_2) else 0)) % 2))
    result = ''.join(c)
    return result.lstrip('0') if len(result) <= 173 else result[(len(result) - 173):]


def multiply_polynomials(poly_1, poly_2, mod_poly):
    deg_poly1 = len(poly_1) - 1
    deg_poly2 = len(poly_2) - 1
    result = [0] * (deg_poly1 + deg_poly2 + 1)
    for i in range(deg_poly1 + 1):
        for j in range(deg_poly2 + 1):
            result[i + j] ^= int(poly_1[i]) & int(poly_2[j])
    while result and result[0] == 0:
        result.pop(0)
    result = ''.join(map(str, result))
    result = binary_division(result, int(mod_poly, 2))
    return result


def square(poly_1, mod_poly):
    sq_ = multiply_polynomials(poly_1, poly_1, mod_poly)
    return sq_


def binary_division(dividend, divisor):
    quotient_ = 0
    remainder_ = int(dividend, 2)
    while remainder_ >= divisor:
        shift = len(bin(remainder_)) - len(bin(divisor))
        remainder_ ^= (divisor << shift)
        quotient_ ^= (1 << shift)
    remainder_ = bin(remainder_)[2:]
    while len(remainder_) < 173:
        remainder_ = remainder_.zfill(173)
    return remainder_


def power_poly(poly_1, poly_3, mod_poly):
    result = '1'
    binary_exponent = ''.join(map(str, poly_3))
    for bit in binary_exponent[::-1]:
        if bit == '1':
            result = multiply_polynomials(result, poly_1, mod_poly)
        poly_1 = square(poly_1, mod_poly)
    return result


def reverse(poly_1):
    power_reverse = 2 ** 173 - 2
    power_reverse = bin(power_reverse)[2:]
    power_reverse = str(power_reverse)
    return power_poly(poly_1, power_reverse, mod)


def trace(poly):
    result = 0
    for char in poly:
        result += int(char)
    return result % 2


poly1 = str(input("Enter the first polynom: "))
poly2 = str(input("Enter the second polynom: "))
poly3 = str(input("Enter the third polynom: "))
mod = ('100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
       '000000000000000000000000000000000000000000000000000010000000111')


add_result, add_time = measure_time(addition, poly1, poly2)
print(f'Addition:  {add_result}')
print(f'Time taken for Addition: {add_time} seconds')

mul_result, mul_time = measure_time(multiply_polynomials, poly1, poly2, mod)
print(f'Multiply:  {mul_result}')
print(f'Time taken for Multiply: {mul_time} seconds')

sq_result, sq_time = measure_time(square, poly1, mod)
print(f'Square:  {sq_result}')
print(f'Time taken for Square: {sq_time} seconds')

reverse_result, reverse_time = measure_time(reverse, poly1)
print(f'Reverse:  {reverse_result}')
print(f'Time taken for Reverse: {reverse_time} seconds')

pow_result, pow_time = measure_time(power_poly, poly1, poly3, mod)
print(f'Power:  {pow_result}')
print(f'Time taken for Power: {pow_time} seconds')

# trace_result = trace(poly1)
# print(f'Trace: {trace_result}')
