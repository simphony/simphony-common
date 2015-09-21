import numpy as np
from enum import IntEnum


class BravaisLattice(IntEnum):
    """The 3D Bravais lattices"""
    CUBIC = 0
    BODY_CENTERED_CUBIC = 1
    FACE_CENTERED_CUBIC = 2
    RHOMBOHEDRAL = 3
    TETRAGONAL = 4
    BODY_CENTERED_TETRAGONAL = 5
    HEXAGONAL = 6
    ORTHORHOMBIC = 7
    BODY_CENTERED_ORTHORHOMBIC = 8
    FACE_CENTERED_ORTHORHOMBIC = 9
    BASE_CENTERED_ORTHORHOMBIC = 10
    MONOCLINIC = 11
    BASE_CENTERED_MONOCLINIC = 12
    TRICLINIC = 13


class PrimitiveCell(object):
    """
    A primitive cell of a Bravais lattice.
    The cell edges are represented with primitive vectors.

    Primitive cells can be configured either by providing the
    primitive vectors explicitly (default) or by providing appropriate
    (conventional) unit cell edge parameters (for the class methods).

    Attributes
    ----------
    p1, p2, p3: 3 x float[3]
        primitive vectors

    bravais_lattice: BravaisLattice(IntEnum)
        the 3D Bravais lattice for which the primitive cell is defined,
        i.e. not the symmetry group or type of the primitive cell itself
    """

    def __init__(self, p1, p2, p3, bravais_lattice):
        """
        Configure an arbitrary primitive cell.
        The cell edges are represented with primitive vectors.

        Parameters
        ----------
        p1, p2, p3: 3 x float[3]
            primitive vectors
        bravais_lattice: BravaisLattice(IntEnum)
            the 3D Bravais lattice for which the primitive cell is defined

        Raises
        ------
        ValueError
           if an edge length is not strictly positive,
           if the edges are parallel to each other,
           if the volume of the cell is zero
        """
        a = np.sqrt(np.dot(p1, p1))
        b = np.sqrt(np.dot(p2, p2))
        c = np.sqrt(np.dot(p3, p3))

        if np.any(np.isclose((a, b, c), (0, 0, 0))):
            message = 'Edge lengths must be strictly positive'
            raise ValueError(message)

        cos1 = np.dot(p2, p3)/(b*c)
        cos2 = np.dot(p1, p3)/(a*c)
        cos3 = np.dot(p1, p2)/(a*b)

        if np.any(np.isclose(np.absolute((cos1, cos2, cos3)), (1, 1, 1))):
            message = 'Edges must not be parallel to each other'
            raise ValueError(message)

        self._p1 = p1
        self._p2 = p2
        self._p3 = p3

        if np.isclose(self.volume, 0):
            message = 'Cell volume must be non-zero'
            raise ValueError(message)

        self._bravais_lattice = bravais_lattice

    @classmethod
    def for_cubic_lattice(cls, a):
        """
        Create a primitive cell for a cubic lattice.

        Parameters
        ----------
        a: float
            (conventional) unit cell edge length

        Returns
        -------
        A primitive cell for a cubic lattice

        Raises
        ------
        ValueError
           if the edge length is not strictly positive
        """
        if a <= 0:
            message = 'The edge length must be strictly positive'
            raise ValueError(message)

        return cls((a, 0, 0), (0, a, 0), (0, 0, a), BravaisLattice.CUBIC)

    @classmethod
    def for_body_centered_cubic_lattice(cls, a):
        """
        Create a primitive cell for a body-centered cubic lattice.

        Parameters
        ----------
        a: float
            (conventional) unit cell edge length

        Returns
        -------
        A primitive cell for a body-centered cubic lattice

        Raises
        ------
        ValueError
           if the edge length is not strictly positive
        """
        if a <= 0:
            message = 'The edge length must be strictly positive'
            raise ValueError(message)

        return cls((a, 0, 0), (0, a, 0), (a/2, a/2, a/2),
                   BravaisLattice.BODY_CENTERED_CUBIC)

    @classmethod
    def for_face_centered_cubic_lattice(cls, a):
        """
        Create a primitive cell for a face-centered cubic lattice.

        Parameters
        ----------
        a: float
            (conventional) unit cell edge length

        Returns
        -------
        A primitive cell for a face-centered cubic lattice

        Raises
        ------
        ValueError
           if the edge length is not strictly positive
        """
        if a <= 0:
            message = 'The edge length must be strictly positive'
            raise ValueError(message)

        return cls((0, a/2, a/2), (a/2, 0, a/2), (a/2, a/2, 0),
                   BravaisLattice.FACE_CENTERED_CUBIC)

    @classmethod
    def for_rhombohedral_lattice(cls, a, alpha):
        """
        Create a primitive cell for a rhombohedral lattice.

        Parameters
        ----------
        a: float
            (conventional) unit cell edge length

        alpha: float
            angle between the (conventional) unit cell edges (in radians)

        Returns
        -------
        A primitive cell for a rhombohedral lattice

        Raises
        ------
        ValueError
           if the edge length is not strictly positive,
           if the edges are parallel to each other
        """
        if a <= 0:
            message = 'The edge length must be strictly positive'
            raise ValueError(message)

        angle1 = alpha % np.pi
        if np.allclose(angle1, 0) or np.allclose(angle1, np.pi):
            message = 'Edges must not be parallel to each other'
            raise ValueError(message)

        cosa = np.cos(alpha)
        sina = np.sin(alpha)

        p1 = (a, 0, 0)
        p2 = (a*cosa, a*sina, 0)
        p3 = (a*cosa, a*(cosa-cosa**2) / sina,
              a*np.sqrt(sina**2 - ((cosa-cosa**2) / sina)**2))
        return cls(p1, p2, p3, BravaisLattice.RHOMBOHEDRAL)

    @classmethod
    def for_tetragonal_lattice(cls, a, c):
        """
        Create a primitive cell for a tetragonal lattice.

        Parameters
        ----------
        a, c: 2 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for a tetragonal lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0 or c <= 0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        return cls((a, 0, 0), (0, a, 0), (0, 0, c),
                   BravaisLattice.TETRAGONAL)

    @classmethod
    def for_body_centered_tetragonal_lattice(cls, a, c):
        """
        Create a primitive cell for a body-centered tetragonal lattice.

        Parameters
        ----------
        a, c: 2 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for a body-centered tetragonal lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0 or c <= 0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        return cls((a, 0, 0), (0, a, 0), (a/2, a/2, c/2),
                   BravaisLattice.BODY_CENTERED_TETRAGONAL)

    @classmethod
    def for_hexagonal_lattice(cls, a, c):
        """
        Create a primitive cell for a hexagonal lattice.

        Parameters
        ----------
        a, c: 2 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for a hexagonal lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0 or c <= 0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        return cls((a, 0, 0), (a/2, a*np.sqrt(3)/2, 0), (0, 0, c),
                   BravaisLattice.HEXAGONAL)

    @classmethod
    def for_orthorhombic_lattice(cls, a, b, c):
        """
        Create a primitive cell for an orthorhombic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for an orthorhombic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0 or b <= 0 or c <= 0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        return cls((a, 0, 0), (0, b, 0), (0, 0, c),
                   BravaisLattice.ORTHORHOMBIC)

    @classmethod
    def for_body_centered_orthorhombic_lattice(cls, a, b, c):
        """
        Create a primitive cell for a body-centered orthorhombic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for a body-centered orthorhombic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0 or b <= 0 or c <= 0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        return cls((a, 0, 0), (0, b, 0), (a/2, b/2, c/2),
                   BravaisLattice.BODY_CENTERED_ORTHORHOMBIC)

    @classmethod
    def for_face_centered_orthorhombic_lattice(cls, a, b, c):
        """
        Create a primitive cell for a face-centered orthorhombic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for a face-centered orthorhombic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0 or b <= 0 or c <= 0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        return cls((0, b/2, c/2), (a/2, 0, c/2), (a/2, b/2, 0),
                   BravaisLattice.FACE_CENTERED_ORTHORHOMBIC)

    @classmethod
    def for_base_centered_orthorhombic_lattice(cls, a, b, c):
        """
        Create a primitive cell for a base-centered orthorhombic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for a base-centered orthorhombic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0 or b <= 0 or c <= 0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        return cls((a, 0, 0), (a/2, b/2, 0), (0, 0, c),
                   BravaisLattice.BASE_CENTERED_ORTHORHOMBIC)

    @classmethod
    def for_monoclinic_lattice(cls, a, b, c, beta):
        """
        Create a primitive cell for a monoclinic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths

        beta: float
            angle between the (conventional) unit cell edges (in radians),

        Returns
        -------
        A primitive cell for a monoclinic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive,
           if the edges are parallel to each other
        """
        if a <= 0 or b <= 0 or c <= 0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        angle1 = beta % np.pi
        if np.allclose(angle1, 0) or np.allclose(angle1, np.pi):
            message = 'Edges must not be parallel to each other'
            raise ValueError(message)

        return cls((a*np.sin(beta), 0, a*np.cos(beta)), (0, b, 0), (0, 0, c),
                   BravaisLattice.MONOCLINIC)

    @classmethod
    def for_base_centered_monoclinic_lattice(cls, a, b, c, beta):
        """
        Create a primitive cell for a base-centered monoclinic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths

        beta: float
            angle between the (conventional) unit cell edges (in radians)

        Returns
        -------
        A primitive cell for a base-centered monoclinic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive,
           if the edges are parallel to each other
        """
        if a <= 0 or b <= 0 or c <= 0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        angle1 = beta % np.pi
        if np.allclose(angle1, 0) or np.allclose(angle1, np.pi):
            message = 'Edges must not be parallel to each other'
            raise ValueError(message)

        return cls((a*np.sin(beta), 0, a*np.cos(beta)),
                   (a*np.sin(beta)/2, b/2, a*np.cos(beta)/2), (0, 0, c),
                   BravaisLattice.BASE_CENTERED_MONOCLINIC)

    @classmethod
    def for_triclinic_lattice(cls, a, b, c, alpha, beta, gamma):
        """
        Create a primitive cell for a triclinic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths
        alpha, beta, gamma: 3 x float
            angles between the (conventional) unit cell edges (in radians)

        Returns
        -------
        A primitive cell for a triclinic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive,
           if the edges are parallel to each other
        """
        if a <= 0 or b <= 0 or c <= 0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        a1 = alpha % np.pi
        a2 = beta % np.pi
        a3 = gamma % np.pi

        if np.any(np.isclose((a1, a2, a3), (0, 0, 0))) or \
           np.any(np.isclose((a1, a2, a3), (np.pi, np.pi, np.pi))):
            message = 'Edges must not be parallel to each other'
            raise ValueError(message)

        if np.any(np.isclose((a1 + a2, a1 + a3, a2 + a3), (a3, a2, a1))):
            message = 'Sum of any two angles must be larger than the third'
            raise ValueError(message)

        cosa = np.cos(alpha)
        cosb = np.cos(beta)
        sinb = np.sin(beta)
        cosg = np.cos(gamma)
        sing = np.sin(gamma)

        p1 = (a, 0, 0)
        p2 = (b*cosg, b*sing, 0)
        p3 = (c*cosb, c*(cosa-cosb*cosg) / sing,
              c*np.sqrt(sinb**2 - ((cosa-cosb*cosg) / sing)**2))
        return cls(p1, p2, p3, BravaisLattice.TRICLINIC)

    @property
    def bravais_lattice(self):
        return self._bravais_lattice

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2

    @property
    def p3(self):
        return self._p3

    @property
    def volume(self):
        return np.absolute(np.dot(self._p1, np.cross(self._p2, self._p3)))
