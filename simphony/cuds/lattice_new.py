import numpy as np
from math import sqrt
from simphony.cuds.abc_lattice import ABCLattice
from simphony.core.cuds_item import CUDSItem
from simphony.core.data_container import DataContainer
from simphony.cuds.primitive_cell import PrimitiveCell as pc


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
        name of lattice
    size : int[3]
        lattice dimensions
    origin : float[3]
        lattice origin
    prim_cell : PrimitiveCell
        primitive cell specifying the 3D Bravais lattice
    data : DataContainer
        high level CUBA data assigned to lattice
    """

    def __init__(self, name, size, origin, prim_cell):
        self.name = name
        self._size = size[0], size[1], size[2]
        self._origin = np.array((origin[0], origin[1], origin[2]),
                                dtype=np.float)
        self._prim_cell = prim_cell
        self._dcs = np.empty(size, dtype=object)
        self._data = DataContainer()

        self._items_count = {
            CUDSItem.NODE: lambda: self._size
        }

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
        nodes : iterable of LatticeNode objects
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
        p1 = self.prim_vec.p1
        p2 = self.prim_vec.p2
        p3 = self.prim_vec.p3
        return self.origin + index[0]*p1 + index[1]*p2 + index[2]*p3

    def count_of(self, item_type):
        """ Return the count of item_type in the container.

        Parameters
        ----------
        item_type : CUDSItem
            The CUDSItem enum of the type of the items to return the count of.

        Returns
        -------
        count : int
            The number of items of item_type in the container.

        Raises
        ------
        ValueError :
            If the type of the item is not supported in the current
            container.

        """
        try:
            return np.prod(self._items_count[item_type]())
        except KeyError:
            error_str = "Trying to obtain count a of non-supported item: {}"
            raise ValueError(error_str.format(item_type))

    @property
    def size(self):
        return self._size

    @property
    def origin(self):
        return self._origin

    @property
    def prim_cell(self):
        return self._prim_cell

    @property
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, value):
        self._data = DataContainer(value)


def make_cubic_lattice(name, h, size, org=(0, 0, 0)):
    """Create and return a 3D (primitive) cubic lattice.

    Parameters
    ----------
    name : str
    h : float
        lattice spacing
    size : int[3]
        Number of lattice nodes in each axis direction.
    org : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    pcell = pc.create_cell_cubic_lattice(h)
    return Lattice(name, 'Cubic', size, org, pcell)


def make_body_cent_cubic_lattice(name, h, size, org=(0, 0, 0)):
    """Create and return a 3D body-centered cubic lattice.

    Parameters
    ----------
    name : str
    h : float
        lattice spacing
    size : int[3]
        Number of lattice nodes in each axis direction.
    org : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    pcell = pc.create_cell_body_cent_cubic_lattice(h)
    return Lattice(name, 'Body-Centered Cubic', size, org, pcell)


def make_face_cent_cubic_lattice(name, h, size, org=(0, 0, 0)):
    """Create and return a 3D face-centered cubic lattice.

    Parameters
    ----------
    name : str
    h : float
        lattice spacing
    size : int[3]
        Number of lattice nodes in each axis direction.
    org : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    pcell = pc.create_cell_face_cent_cubic_lattice(h)
    return Lattice(name, 'Face-Centered Cubic', size, org, pcell)


def make_orthorhombic_lattice(name, hs, size, org=(0, 0, 0)):
    """Create and return a 3D (primitive) orthorhombic lattice.

    Parameters
    ----------
    name : str
    hs : float[3]
        lattice spacings in each axis direction
    size : int[3]
        Number of lattice nodes in each axis direction.
    org : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.

    """
    pcell = pc.create_cell_orthorhombic_lattice(hs[0],hs[1],hs[2])
    return Lattice(name, 'Orthorhombic', size, org, pcell)

    
def make_body_cent_orthorhombic_lattice(name, hs, size, org=(0, 0, 0)):
    """Create and return a 3D body-centered orthorhombic lattice.

    Parameters
    ----------
    name : str
    hs : float[3]
        lattice spacings in each axis direction
    size : int[3]
        Number of lattice nodes in each axis direction.
    org : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.

    """
    pcell = pc.create_cell_body_cent_orthorhombic_lattice(hs[0],hs[1],hs[2])
    return Lattice(name, 'Body-Centered Orthorhombic', size, org, pcell)


def make_face_cent_orthorhombic_lattice(name, hs, size, org=(0, 0, 0)):
    """Create and return a 3D face-centered orthorhombic lattice.

    Parameters
    ----------
    name : str
    hs : float[3]
        lattice spacings in each axis direction
    size : int[3]
        Number of lattice nodes in each axis direction.
    org : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.

    """
    pcell = pc.create_cell_face_cent_orthorhombic_lattice(hs[0],hs[1],hs[2])
    return Lattice(name, 'Face-Centered Orthorhombic', size, org, pcell)


def make_base_cent_orthorhombic_lattice(name, hs, size, org=(0, 0, 0)):
    """Create and return a 3D base-centered orthorhombic lattice.

    Parameters
    ----------
    name : str
    hs : float[3]
        lattice spacings in each axis direction
    size : int[3]
        Number of lattice nodes in each axis direction.
    org : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.

    """
    pcell = pc.create_cell_base_cent_orthorhombic_lattice(hs[0],hs[1],hs[2])
    return Lattice(name, 'Base-Centered Orthorhombic', size, org, pcell)


def make_hexagonal_lattice(name, hxy, hz, size, org=(0, 0, 0)):
    """Create and return a 3D (primitive) hexagonal lattice.

    Parameters
    ----------
    name : str
    hxy : float
        lattice spacing in the xy-plane
    hz : float
        lattice spacing in the z-direction
    size : int[3]
        Number of lattice nodes in each axis direction.
    org : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    pcell = pc.create_cell_hexagonal_lattice(hxy, hz)
    return Lattice(name, 'Hexagonal', size, org, pcell)
