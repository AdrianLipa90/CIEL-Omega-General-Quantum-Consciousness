"""Implementation of the Lie4 algebra for 4D transformations.

This module provides the fundamental Lie algebra operations for the CIEL system,
including Lie4 elements, basis generation, and algebraic operations.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np
try:
    from scipy.linalg import expm as _scipy_expm
except ModuleNotFoundError:  # pragma: no cover
    _scipy_expm = None


def expm(a: np.ndarray) -> np.ndarray:
    if _scipy_expm is not None:
        return _scipy_expm(a)

    w, v = np.linalg.eig(a)
    exp_w = np.exp(w)
    exp_a = v @ np.diag(exp_w) @ np.linalg.inv(v)

    if np.isrealobj(a) and np.max(np.abs(np.imag(exp_a))) < 1e-12:
        return np.real(exp_a)
    return exp_a


@dataclass
class Lie4Element:
    """Represents an element of the Lie4 algebra."""
    basis_elements: np.ndarray  # 4x4 matrix representing the element
    
    def __post_init__(self):
        if self.basis_elements.shape != (4, 4):
            raise ValueError("Lie4 element must be a 4x4 matrix")
        # Ensure the matrix is antisymmetric
        if not np.allclose(self.basis_elements, -self.basis_elements.T):
            raise ValueError("Lie4 element must be antisymmetric")
    
    def __add__(self, other: 'Lie4Element') -> 'Lie4Element':
        return Lie4Element(self.basis_elements + other.basis_elements)
    
    def __sub__(self, other: 'Lie4Element') -> 'Lie4Element':
        return Lie4Element(self.basis_elements - other.basis_elements)
    
    def __mul__(self, scalar: float) -> 'Lie4Element':
        return Lie4Element(self.basis_elements * scalar)
    
    def __rmul__(self, scalar: float) -> 'Lie4Element':
        return self * scalar
    
    def commutator(self, other: 'Lie4Element') -> 'Lie4Element':
        """Compute the Lie bracket [self, other] = self @ other - other @ self"""
        return Lie4Element(
            self.basis_elements @ other.basis_elements - 
            other.basis_elements @ self.basis_elements
        )
    
    def exp(self) -> np.ndarray:
        """Compute the matrix exponential of this Lie algebra element."""
        return expm(self.basis_elements)
    
    @classmethod
    def basis_generator(cls, i: int, j: int) -> 'Lie4Element':
        """Generate a basis element with 1 at position (i,j) and -1 at (j,i)."""
        if i == j or i >= 4 or j >= 4 or i < 0 or j < 0:
            raise ValueError("Invalid basis element indices")
        
        basis = np.zeros((4, 4))
        basis[i, j] = 1.0
        basis[j, i] = -1.0
        return cls(basis)


class Lie4Algebra:
    """Implementation of the Lie4 algebra operations.
    
    This class provides operations for working with the Lie algebra so(4),
    including basis generation, random element creation, and structure constant
    computation.
    """
    
    DIMENSION = 6  # Number of independent generators in so(4)
    
    def __init__(self):
        # Generate the standard basis for so(4)
        self.basis = []
        for i in range(4):
            for j in range(i+1, 4):
                self.basis.append(Lie4Element.basis_generator(i, j))
    
    def random_element(self) -> Lie4Element:
        """Generate a random element of the Lie4 algebra."""
        coeffs = np.random.randn(self.DIMENSION)
        element = Lie4Element(np.zeros((4, 4)))
        for c, basis in zip(coeffs, self.basis):
            element += c * basis
        return element
    
    def structure_constants(self) -> np.ndarray:
        """Compute the structure constants of the algebra.
        
        Returns:
            A 3D numpy array f_ijk where [e_i, e_j] = sum_k f_ijk e_k
        """
        f = np.zeros((self.DIMENSION, self.DIMENSION, self.DIMENSION))
        for i, ei in enumerate(self.basis):
            for j, ej in enumerate(self.basis):
                # [ei, ej] = sum_k f_ijk ek
                comm = ei.commutator(ej)
                # Project onto each basis element to find the coefficients
                for k, ek in enumerate(self.basis):
                    f[i, j, k] = np.trace(comm.basis_elements @ ek.basis_elements.T) / 2.0
        return f
