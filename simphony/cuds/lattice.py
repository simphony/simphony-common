import numpy as np
from math import sqrt
from simphony.cuds.abstractlattice import ABCLattice
from simphony.core.data_container import DataContainer


class LatticeNode(object):
    """A single node of a lattice.

    Attributes
    ----------
    index : tuple of int[3]
        node index coordinate
    data : DataContainer

    """
    def __init__(self, index, data=None):
        self.index = index[0], index[1], index[2]

        if data is None:
            self.data = DataContainer()
        else:
            self.data = DataContainer(data)


class Lattice(ABCLattice):
    """A Bravais lattice. Stores references to data
    containers (node related data).

    Attributes
    ----------
    name : str
        name of the lattice
    type : str
        Bravais lattice type (should agree with the base_vect below).
    base_vect : float[3]
        defines a Bravais lattice
        (an alternative for primitive vectors).
    size : int[3]
        number of lattice nodes in the direction of each axis.
    origin : float[3]
        origin of lattice

    """

    def __init__(self, name, type, base_vect, size, origin):
        self.name = name
        self._type = type
        self._base_vect = np.array((base_vect[0], base_vect[1],
                                    base_vect[2]), dtype=np.float)
        self._size = size[0], size[1], size[2]
        self._origin = np.array((origin[0], origin[1], origin[2]),
                                dtype=np.float)
        self._dcs = np.empty(size, dtype=object)
        self._data = DataContainer()

    def get_node(self, index):
        """Get a copy of the node corresponding to the given index.

        Parameters
        ----------
        index : int[3]
            node index coordinate

        Returns
        -------
        A reference to a LatticeNode object

        """
        tuple_index = tuple(index)
        if tuple_index[0] < 0 or tuple_index[1] < 0 or tuple_index[2] < 0:
            raise IndexError('invalid index: {}'.format(tuple_index))
        return LatticeNode(tuple_index, self._dcs[tuple_index])

    def update_nodes(self, nodes):
        """Update the corresponding lattice nodes (data copied).

        Parameters
        ----------
        nodes : an iterator to a LatticeNode objects
            reference to LatticeNode objects from where the data is copied
            to the Lattice

        """
        for node in nodes:
            index = node.index
            if any(value < 0 for value in index):
                raise IndexError('invalid index: {}'.format(index))
            self._dcs[index] = DataContainer(node.data)

    def iter_nodes(self, indices=None):
        """Get an iterator over the LatticeNodes described by the indices.

        Parameters
        ----------
        indices : iterable set of int[3], optional
            When indices (i.e. node index coordinates) are provided, then nodes
            are returned in the same order of the provided indices. If indices
            is None, there is no restriction on the order the nodes that are
            returned.

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
        index : int[3]
            node index coordinate

        Returns
        -------
        float[3]

        """
        if self._type == 'Hexagonal':
            xorigin, yorigin, zorigin = self.origin
            xspace, yspace, zspace = self.base_vect
            x = xorigin + index[0] * xspace + 0.5 * xspace * index[1]
            y = yorigin + index[1] * yspace
            z = zorigin
            return x, y, z
        else:
            return self.origin + self.base_vect*np.array(index)

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

    @property
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, value):
        self._data = DataContainer(value)


def make_hexagonal_lattice(name, h, size, origin=(0, 0, 0)):
    """Create and return a 2D hexagonal lattice embedded on the XY-plane
    in 3D.

    Parameters
    ----------
    name : str
    h : float
        lattice spacing
    size : int[2]
        Number of lattice nodes in each axis direction.
    origin : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.

    """
    return Lattice(name, 'Hexagonal', (0.5*h, 0.5*sqrt(3)*h, 0),
                   tuple(size)+(1,), (origin[0], origin[1])+(0,))


def make_square_lattice(name, h, size, origin=(0, 0, 0)):
    """Create and return a 2D square lattice embedded on the XY-plane
    in 3D.

    Parameters
    ----------
    name : str
    h : float
        lattice spacing
    size : int[2]
        Number of lattice nodes in each axis direction.
    origin : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.

    """
    return Lattice(name, 'Square', (h, h, 0), tuple(size)+(1,),
                   (origin[0], origin[1])+(0,))


def make_rectangular_lattice(name, hs, size, origin=(0, 0, 0)):
    """Create and return a 2D rectangular lattice embedded on the XY-plane
    in 3D.

    Parameters
    ----------
    name : str
    hs : float[2]
        lattice spacings in each axis direction
    size : int[2]
        Number of lattice nodes in each axis direction.
    origin : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.

    """
    return Lattice(name, 'Rectangular', tuple(hs)+(0,), tuple(size)+(1,),
                   (origin[0], origin[1])+(0,))


def make_cubic_lattice(name, h, size, origin=(0, 0, 0)):
    """Create and return a 3D cubic lattice.

    Parameters
    ----------
    name : str
    h : float
        lattice spacing
    size : int[3]
        Number of lattice nodes in each axis direction.
    origin : float[3], default value = (0, 0, 0)
        lattice origin

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
    name : str
    hs : float[3]
        lattice spacings in each axis direction
    size : int[3]
        Number of lattice nodes in each axis direction.
    origin : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.

    """
    return Lattice(name, 'OrthorombicP', hs, size, origin)
