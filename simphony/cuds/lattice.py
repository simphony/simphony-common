import numpy as np
from math import sqrt
from simphony.core.data_container import DataContainer


class LatticeNode:
    """
    A single node of a lattice.

    Attributes
    ----------
    id :  tuple of D x int
        Node index coordinate
    data : DataContainer


    """
    def __init__(self, id, data=None):
        self.id = tuple(id)

        if data is None:
            self.data = DataContainer()
        else:
            self.data = DataContainer(data)


class Lattice(object):
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

    def get_node(self, id):
        """Get a copy of the node corresponding to the given id.

        Parameters
        ----------
        id: tuple of D x int (node index coordinate)

        Returns
        -------
        A reference to a LatticeNode object
        """
        tuple_id = tuple(id)
        return LatticeNode(tuple_id, self._dcs[tuple_id])

    def update_node(self, lat_node):
        """Update the corresponding lattice node (data copied).

        Parameters
        ----------
        lat_node: reference to a LatticeNode object
            data copied from the given node
        """
        id = lat_node.id
        self._dcs[id] = DataContainer(lat_node.data)

    def iter_nodes(self, ids=None):
        """Get an iterator over the LatticeNodes described by the ids.

        Parameters
        ----------
        ids: iterable set of D x int (node index coordinates)

        Returns
        -------
        A generator for LatticeNode objects
        """
        if ids is None:
            for id, val in np.ndenumerate(self._dcs):
                yield self.get_node(id)
        else:
            for id in ids:
                yield self.get_node(id)

    def get_coordinate(self, id):
        """Get coordinate of the given index coordinate.

        Parameters
        ----------
        id: D x int (node index coordinate)

        Returns
        -------
        D x float
        """
        return self.origin + self.base_vect*np.array(id)


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
