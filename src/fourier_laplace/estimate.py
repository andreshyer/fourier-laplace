from numpy import array
from math import cos, sin, pi, sqrt


def estimate(z_values: array, P: float, a_constants: list, b_constants: list):
    num_constants = len(a_constants)
    results = []

    for i in range(len(z_values)):
        z = z_values[i]

        if z < 0.3:
            results.append(sqrt(2 * z - z ** 2))

        else:
            x_calc = 0.0
            for n in range(num_constants):
                a_n = a_constants[n]
                b_n = b_constants[n]
                if n == 0:
                    x_calc += a_n
                else:
                    x_calc += a_n * cos(2 * pi * n * z / P)
                    x_calc += b_n * sin(2 * pi * n * z / P)
            results.append(x_calc)

    return results