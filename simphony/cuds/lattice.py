import numpy as np
from math import sqrt
from simphony.cuds.abstractlattice import ABCLattice
from simphony.core.data_container import DataContainer


class LatticeNode:
    """
    A single node of a lattice.

    Attributes
    ----------
    index: tuple of D x int
        Node index coordinate
    data : DataContainer


    """
    def __init__(self, index, data=None):
        self.index = tuple(index)

        if data is None:
            self.data = DataContainer()
        else:
            self.data = DataContainer(data)


class Lattice(ABCLattice):
    """
    A Bravais lattice;
    stores references to data containers (node related data).

    Parameters
    ----------
    name: str
    type: str
        Bravais lattice type (should agree with the base_vect below).
    base_vect: D x float
        defines a Bravais lattice (an alternative for primitive vectors).
    size: D x size
        number of lattice nodes (in the direction of each axis).
    origin: D x float

    """
    def __init__(self, name, type, base_vect, size, origin):
        self.name = name
        self._type = type
        self._base_vect = np.array(base_vect, dtype=np.float)
        self._size = np.array(size, dtype=np.uint32)
        self._origin = np.array(origin, dtype=np.float)
        self._dcs = np.empty(size, dtype=object)

    @property
    def type(self):
        return self._type

    @property
    def base_vect(self):
        return self._base_vect

    @property
    def size(self):
        return self._size

    @property
    def origin(self):
        return self._origin

    def get_node(self, index):
        """Get a copy of the node corresponding to the given index.

        Parameters
        ----------
        index: tuple of D x int (node index coordinate)

        Returns
        -------
        A reference to a LatticeNode object
        """
        tuple_index = tuple(index)
        return LatticeNode(tuple_index, self._dcs[tuple_index])

    def update_node(self, lat_node):
        """Update the corresponding lattice node (data copied).

        Parameters
        ----------
        lat_node: reference to a LatticeNode object
            data copied from the given node
        """
        index = lat_node.index
        self._dcs[index] = DataContainer(lat_node.data)

    def iter_nodes(self, indices=None):
        """Get an iterator over the LatticeNodes described by the indices.

        Parameters
        ----------
        indices: iterable set of D x int (node index coordinates)

        Returns
        -------
        A generator for LatticeNode objects
        """
        if indices is None:
            for index, val in np.ndenumerate(self._dcs):
                yield self.get_node(index)
        else:
            for index in indices:
                yield self.get_node(index)

    def get_coordinate(self, index):
        """Get coordinate of the given index coordinate.

        Parameters
        ----------
        index: D x int (node index coordinate)

        Returns
        -------
        D x float
        """
        return self.origin + self.base_vect*np.array(index)


def make_hexagonal_lattice(name, h, size, origin=(0, 0)):
    """Create and return a 2D hexagonal lattice.

    Parameters
    ----------
    name: string
    h: float
        lattice spacing.
    size: 2 x int
        number of lattice nodes (in each axis direction).
    origin: 2 x float (default value = (0,0))
        lattice origin.

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    return Lattice(name, 'Hexagonal', (0.5*h, 0.5*sqrt(3)*h), size, origin)


def make_square_lattice(name, h, size, origin=(0, 0)):
    """Create and return a 2D square lattice.

    Parameters
    ----------
    name: string
    h: float
        lattice spacing.
    size: 2 x int
        number of lattice nodes (in each axis direction).
    origin: 2 x float (default value = (0,0))
        lattice origin.

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    return Lattice(name, 'Square', (h, h), size, origin)


def make_rectangular_lattice(name, hs, size, origin=(0, 0)):
    """Create and return a 2D rectangular lattice.

    Parameters
    ----------
    name: string
    hs: 2 x float
        lattice spacings (in each axis direction).
    size: 2 x int
        number of lattice nodes (in each axis direction).
    origin: 2 x float (default value = (0,0))
        lattice origin.

    lattice : Lattice
        A reference to a Lattice object.
    """
    return Lattice(name, 'Rectangular', hs, size, origin)


def make_cubic_lattice(name, h, size, origin=(0, 0, 0)):
    """Create and return a 3D cubic lattice.

    Parameters
    ----------
    name: string
    h: float
        lattice spacing.
    size: 3 x int
        number of lattice nodes (in each axis direction).
    origin: 3 x float (default value = (0,0,0))
        lattice origin.

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    return Lattice(name, 'Cubic', (h, h, h), size, origin)


def make_orthorombicp_lattice(name, hs, size, origin=(0, 0, 0)):
    """Create and return a 3D orthorombic primitive lattice.

    Parameters
    ----------
    name: string
    hs: 3 x float
        lattice spacings (in each axis direction).
    size: 3 x int
        number of lattice nodes (in each axis direction).
    origin: 3 x float (default value = (0,0,0))
        lattice origin.

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.

    """
    return Lattice(name, 'OrthorombicP', hs, size, origin)
