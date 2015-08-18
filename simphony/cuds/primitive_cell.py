import numpy as np
from enum import Enum


class BravaisLattice(Enum):
    """The 3D Bravais lattices"""
    CUBIC = 0
    BODY_CENTERED_CUBIC = 1
    FACE_CENTERED_CUBIC = 2
    RHOMBOHEDRAL = 3
    HEXAGONAL = 4
    TETRAGONAL = 5
    BODY_CENTERED_TETRAGONAL = 6
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
    p1, p2, p3: 3 x 3D vector
        primitive vectors

    bravais_lattice: BravaisLattice(Enum)
        the 3D Bravais lattice for which the primitive cell is defined,
        i.e. not the symmetry group or type of the primitive cell itself
    """
   
    def __init__(self, p1, p2, p3):
        """
        Configure an arbitrary primitive cell.
        The cell edges are represented with primitive vectors.
        
        Parameters
        ----------
        p1, p2, p3: 3 x 3D vector
            primitive vectors

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

        if np.any(np.isclose(np.absolute((cos1, cos2, cos3)), (1, 1, 1)):
            message = 'Edges must not be parallel to each other'
            raise ValueError(message)
        
        self._p1 = p1
        self._p2 = p2
        self._p3 = p3

        if np.isclose(self.volume(), 0):
            message = 'Cell volume must be non-zero'
            raise ValueError(message)

        self._bravais_lattice = BravaisLattice.TRICLINIC
            
    @classmethod
    def create_cell_cubic_lattice(cls, a):
        """
        Create a primitive cell for a Cubic lattice.

        Parameters
        ----------
        a: float
            (conventional) unit cell edge length

        Returns
        -------
        A primitive cell for a Cubic lattice

        Raises
        ------
        ValueError
           if the edge length is not strictly positive
        """
        if a <= 0.0:
            message = 'The edge length must be strictly positive'
            raise ValueError(message)

        pc = cls(((a, 0, 0), (0, a, 0), (0, 0, a)))
        pc._bravais_lattice = BravaisLattice.CUBIC
        return pc
        
    @classmethod
    def create_cell_body_cent_cubic_lattice(cls, a):
        """
        Create a primitive cell for a Body-centered Cubic lattice.

        Parameters
        ----------
        a: float
            (conventional) unit cell edge length

        Returns
        -------
        A primitive cell for a Body-centered Cubic lattice

        Raises
        ------
        ValueError
           if the edge length is not strictly positive
        """
        if a <= 0.0:
            message = 'The edge length must be strictly positive'
            raise ValueError(message)

        pc = cls(((a, 0, 0), (0, a, 0), (a/2.0, a/2.0, a/2.0)))
        pc._bravais_lattice = BravaisLattice.BODY_CENTERED_CUBIC
        return pc

    @classmethod
    def create_cell_face_cent_cubic_lattice(cls, a):
        """
        Create a primitive cell for a Face-centered Cubic lattice.

        Parameters
        ----------
        a: float
            (conventional) unit cell edge length

        Returns
        -------
        A primitive cell for a Face-centered Cubic lattice

        Raises
        ------
        ValueError
           if the edge length is not strictly positive
        """
        if a <= 0.0:
            message = 'The edge length must be strictly positive'
            raise ValueError(message)

        pc = cls(((0, a/2.0, a/2.0), (a/2.0, 0, a/2.0), (a/2.0, a/2.0, 0)))
        pc._bravais_lattice = BravaisLattice.FACE_CENTERED_CUBIC
        return pc
        
    @classmethod
    def create_cell_rhombohedral_lattice(cls, a, alpha):
        """
        Create a primitive cell for a Rhombohedral lattice.

        Parameters
        ----------
        a: float
            (conventional) unit cell edge length

        alpha: float
            angle between the (conventional) unit cell edges (in radians),

        Returns
        -------
        A primitive cell for a Rhombohedral lattice

        Raises
        ------
        ValueError
           if the edge length is not strictly positive,
           if the edges are parallel to each other
        """
        if a <= 0.0:
            message = 'The edge length must be strictly positive'
            raise ValueError(message)

        angle1 = alpha%np.pi
        if np.allclose(angle1, 0) or
           np.allclose(angle1, np.pi):
            message = 'Edges must not be parallel to each other'
            raise ValueError(message)
        
        pc = cls.create_triclinic_lattice_cell(a, a, a, alpha, alpha, alpha)
        pc._bravais_lattice = BravaisLattice.RHOMBOHEDRAL
        return pc
        
    @classmethod
    def create_cell_hexagonal_lattice(cls, a, c):
        """
        Create a primitive cell for a Hexagonal lattice.

        Parameters
        ----------
        a, c: 2 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for a Hexagonal lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0.0 or c <= 0.0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        pc = cls(((a, 0, 0), (a/2.0, a*np.sqrt(3.0)/2.0, 0), (0, 0, c)))
        pc._bravais_lattice = BravaisLattice.HEXAGONAL
        return pc

    @classmethod
    def create_cell_tetragonal_lattice(cls, a, c):
        """
        Create a primitive cell for a Tetragonal lattice.

        Parameters
        ----------
        a, c: 2 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for a Tetragonal lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0.0 or c <= 0.0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        pc = cls(((a, 0, 0), (0, a, 0), (0, 0, c)))
        pc._bravais_lattice = BravaisLattice.TETRAGONAL
        return pc

    @classmethod
    def create_cell_body_cent_tetragonal_lattice(cls, a, c):
        """
        Create a primitive cell for a Body-centered Tetragonal lattice.

        Parameters
        ----------
        a, c: 2 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for a Body-centered Tetragonal lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0.0 or c <= 0.0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        pc = cls(((a, 0, 0), (0, a, 0), (a/2.0, a/2.0, c/2.0)))
        pc._bravais_lattice = BravaisLattice.BODY_CENTERED_TETRAGONAL
        return pc

    @classmethod
    def create_cell_orthorhombic_lattice(cls, a, b, c):
        """
        Create a primitive cell for a Orthorhombic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for a Orthorhombic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0.0 or b <= 0.0 or c <= 0.0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        pc = cls(((a, 0, 0), (0, b, 0), (0, 0, c)))
        pc._bravais_lattice = BravaisLattice.ORTHORHOMBIC
        return pc

    @classmethod
    def create_cell_body_cent_orthorhombic_lattice(cls, a, b, c):
        """
        Create a primitive cell for a Body-centered Orthorhombic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for a Body-centered Orthorhombic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0.0 or b <= 0.0 or c <= 0.0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        pc = cls(((a, 0, 0), (0, b, 0), (a/2.0, b/2.0, c/2.0)))
        pc._bravais_lattice = BravaisLattice.BODY_CENTERED_ORTHORHOMBIC
        return pc

    @classmethod
    def create_cell_face_cent_orthorhombic_lattice(cls, a, b, c):
        """
        Create a primitive cell for a Face-centered Orthorhombic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for a Face-centered Orthorhombic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0.0 or b <= 0.0 or c <= 0.0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        pc = cls(((0, b/2.0, c/2.0), (a/2.0, 0, c/2.0), (a/2.0, b/2.0, 0)))
        pc._bravais_lattice = BravaisLattice.FACE_CENTERED_ORTHORHOMBIC
        return pc

    @classmethod
    def create_cell_base_cent_orthorhombic_lattice(cls, a, b, c):
        """
        Create a primitive cell for a Base-centered Orthorhombic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths

        Returns
        -------
        A primitive cell for a Base-centered Orthorhombic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive
        """
        if a <= 0.0 or b <= 0.0 or c <= 0.0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        pc = cls(((a, 0, 0), (a/2.0, b/2.0, 0), (0, 0, c)))
        pc._bravais_lattice = BravaisLattice.BASE_CENTERED_ORTHORHOMBIC
        return pc

    @classmethod
    def create_cell_monoclinic_lattice(cls, a, b, c, beta):
        """
        Create a primitive cell for a Monoclinic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths

        beta: float
            angle between the (conventional) unit cell edges (in radians),

        Returns
        -------
        A primitive cell for a Monoclinic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive,
           if the edges are parallel to each other
        """
        if a <= 0.0 or b <= 0.0 or c <= 0.0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        angle1 = beta%np.pi
        if np.allclose(angle1, 0) or
           np.allclose(angle1, np.pi):
            message = 'Edges must not be parallel to each other'
            raise ValueError(message)
        
        pc = cls(((a*np.sin(beta), 0, a*np.cos(beta)), (0, b, 0), (0, 0, c)))
        pc._bravais_lattice = BravaisLattice.MONOCLINIC
        return pc

    @classmethod
    def create_cell_base_cent_monoclinic_lattice(cls, a, b, c, beta):
        """
        Create a primitive cell for a Base-centered Monoclinic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths

        beta: float
            angle between the (conventional) unit cell edges (in radians),

        Returns
        -------
        A primitive cell for a Base-centered Monoclinic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive,
           if the edges are parallel to each other
        """
        if a <= 0.0 or b <= 0.0 or c <= 0.0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        angle1 = beta%np.pi
        if np.allclose(angle1, 0) or
           np.allclose(angle1, np.pi):
            message = 'Edges must not be parallel to each other'
            raise ValueError(message)
        
        pc = cls(((a*np.sin(beta), 0, a*np.cos(beta)),
                  (a*np.sin(beta)/2.0, b/2.0, a*np.cos(beta)/2.0),
                  (0, 0, c)))
        pc._bravais_lattice = BravaisLattice.BASE_CENTERED_MONOCLINIC
        return pc

    @classmethod
    def create_cell_triclinic_lattice(cls, a, b, c, alpha, beta, gamma):
        """
        Create a primitive cell for a Triclinic lattice.

        Parameters
        ----------
        a, b, c: 3 x float
            (conventional) unit cell edge lengths
        alpha, beta, gamma: 3 x float
            angles between the (conventional) unit cell edges (in radians),

        Returns
        -------
        A primitive cell for a Triclinic lattice

        Raises
        ------
        ValueError
           if an edge length is not strictly positive,
           if the edges are parallel to each other
        """
        if a <= 0.0 or b <= 0.0 or c <= 0.0:
            message = 'The edge lengths must be strictly positive'
            raise ValueError(message)

        a1 = alpha%np.pi
        a2 = beta%np.pi
        a3 = gamma%np.pi
        
        if np.any(np.isclose((a1, a2, a3), (0, 0, 0))) or
           np.any(np.isclose((a1, a2, a3), (np.pi, np.pi, np.pi))):
            message = 'Edges must not be parallel to each other'
            raise ValueError(message)

        bcosg = b*np.cos(gamma)
        bsing = b*np.sin(gamma)
        ccosb = c*np.cos(beta)
        ccosa = c*np.cos(alpha)
        
        p1 = (a, 0, 0)
        p2 = (bcosg, bsing, 0)
        
        p3x = ccosb
        p3y = (b*ccosa-p2[0]*p3x)/p2[1]
        p3z = np.sqrt(c*c - (p3x*p3x + p3y*p3y))
        p3 = (p3x, p3y, p3z)
        
        pc = cls(p1, p2, p3)
        return pc
                
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
        return np.absolute(np.dot(self.p1, np.cross(self.p2, self.p3)))
