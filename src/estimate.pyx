from math import cos, sin, pi, sqrt
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def estimate(double[:] z_values, double P, list a_constants, list b_constants):
    cdef Py_ssize_t i, n, num_constants = len(a_constants)
    cdef double x_calc, a_n, b_n
    cdef list results = []

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