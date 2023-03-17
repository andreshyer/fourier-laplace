from pathlib import Path
from numpy import loadtxt, searchsorted, where, array

from .estimate import estimate

# Load data files
a_data = loadtxt(Path(__file__).parent / 'tables/a_data.csv', delimiter=',')
b_data = loadtxt(Path(__file__).parent / 'tables/b_data.csv', delimiter=',')
P_data = loadtxt(Path(__file__).parent / 'tables/P_data.csv', delimiter=',')

class FourierProfile:

    def __init__(self, bond_number: int):        
        if abs(bond_number) > 0.35:
            return ValueError(f"The value of the bond_number, {bond_number}, should be less than 0.35.")
        if bond_number < 0.1:
            return ValueError(f"The value of the bond_number, {bond_number}, should be greater than 0.1.")
        
        self.bond_number: int = bond_number

        self.a_constants = list(self._interp_rows(a_data, bond_number))
        self.b_constants = list(self._interp_rows(b_data, bond_number))
        self.P = self._interp_rows(P_data, bond_number)[0]

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
