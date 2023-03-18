from pathlib import Path
from math import sqrt, cos, sin, pi
from numpy import loadtxt, searchsorted, where, array

# Load data files
a_data = loadtxt(Path(__file__).parent / 'tables/a_data.csv', delimiter=',')
b_data = loadtxt(Path(__file__).parent / 'tables/b_data.csv', delimiter=',')
P_data = loadtxt(Path(__file__).parent / 'tables/P_data.csv', delimiter=',')
max_x_data = loadtxt(Path(__file__).parent / 'tables/max_x_data.csv', delimiter=',')


def estimate(z_values: array, P: float, a_constants: list, b_constants: list):
    num_constants = len(a_constants)
    results = []

    for i in range(len(z_values)):
        z = z_values[i]

        if z < 0.1:
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


class FourierProfile:

    def __init__(self, bond_number: int):        
        if abs(bond_number) > 0.35:
            return ValueError(f"The value of the bond_number, {bond_number}, should be less than 0.35.")
        if bond_number < 0.1:
            return ValueError(f"The value of the bond_number, {bond_number}, should be greater than 0.1.")
        
        self.bond_number: int = bond_number

        # Grab variables
        self.a_constants = list(self._interp_rows(a_data, bond_number))
        self.b_constants = list(self._interp_rows(b_data, bond_number))
        self.P = self._interp_rows(P_data, bond_number)[0]
        self.max_x = self._interp_rows(max_x_data, bond_number)[0]

    @staticmethod
    def _interp_rows(d, bond_number):
        Bo = d[:, 0]
        idx_lower = searchsorted(Bo, bond_number, side='right') - 1
        idx_upper = idx_lower + 1
        lower_row = d[idx_lower, 1:]
        upper_row = d[idx_upper, 1:]
        return lower_row + (bond_number - Bo[idx_lower]) * (upper_row - lower_row) / (Bo[idx_upper] - Bo[idx_lower])

    def estimate(self, z: array) -> array:

        if len(where(z < 0)[0]) > 0:
            raise ValueError("Value of z less than 0 detected")
        if len(where(z > 5)[0]) > 0:
            raise ValueError("Value of z greater than 5 detected")

        return array(estimate(z, self.P, self.a_constants, self.b_constants))
    
    def get_max_x(self) -> float:
        return self.max_x
