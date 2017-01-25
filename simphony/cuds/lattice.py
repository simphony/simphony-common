import uuid
import numpy as np

from ..core import CUBA
from ..core.data_container import DataContainer
from .abc_lattice import ABCLattice
from .lattice_items import LatticeNode
from .primitive_cell import PrimitiveCell


class Lattice(ABCLattice):
    """A Bravais lattice. Stores references to data
    containers (node related data).

    Attributes
    ----------
    name : str
        name of lattice
    primitive_cell : PrimitiveCell
        primitive cell specifying the 3D Bravais lattice
    size : int[3]
        lattice dimensions
    origin : float[3]
        lattice origin
    data : DataContainer
        high level CUBA data assigned to lattice
    """

    cuba_key = CUBA.LATTICE

    def __init__(self, name, primitive_cell, size, origin):
        self.name = name
        self._primitive_cell = primitive_cell
        self._size = size[0], size[1], size[2]
        self._origin = np.array((origin[0], origin[1], origin[2]),
                                dtype=np.float)
        self._dcs = np.empty(size, dtype=object)
        self._data = DataContainer()

        self._items_count = {
            CUBA.NODE: lambda: self._size
        }
        self._uid = uuid.uuid4()

    @property
    def uid(self):
        return self._uid

    def count_of(self, item_type):
        """ Return the count of item_type in the container.

        Parameters
        ----------
        item_type : CUBA
            The CUBA enum of the type of the items to return
            the count of.

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
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, value):
        self._data = DataContainer(value)

    def _get_node(self, index):
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

    def _update_nodes(self, nodes):
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

    def _iter_nodes(self, indices=None):
        """Get an iterator over the LatticeNodes described by the indices.

        Parameters
        ----------
        indices : iterable set of int[3], optional
            When indices (i.e. node index coordinates) are provided, then
            nodes are returned in the same order of the provided indices.
            If indices is None, there is no restriction on the order of the
            returned nodes.

        Returns
        -------
        A generator for LatticeNode objects

        """
        if indices is None:
            for index, val in np.ndenumerate(self._dcs):
                yield self.get(index)
        else:
            for index in indices:
                yield self.get(index)


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
    pc = PrimitiveCell.for_cubic_lattice(h)
    return Lattice(name, pc, size, origin)


def make_body_centered_cubic_lattice(name, h, size, origin=(0, 0, 0)):
    """Create and return a 3D body-centered cubic lattice.

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
    pc = PrimitiveCell.for_body_centered_cubic_lattice(h)
    return Lattice(name, pc, size, origin)


def make_face_centered_cubic_lattice(name, h, size, origin=(0, 0, 0)):
    """Create and return a 3D face-centered cubic lattice.

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
    pc = PrimitiveCell.for_face_centered_cubic_lattice(h)
    return Lattice(name, pc, size, origin)


def make_rhombohedral_lattice(name, h, angle, size, origin=(0, 0, 0)):
    """Create and return a 3D rhombohedral lattice.

    Parameters
    ----------
    name : str
    h : float
        lattice spacing
    angle : float
        angle between the (conventional) unit cell edges (in radians)
    size : int[3]
        Number of lattice nodes in each axis direction.
    origin : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    pc = PrimitiveCell.for_rhombohedral_lattice(h, angle)
    return Lattice(name, pc, size, origin)


def make_tetragonal_lattice(name, hxy, hz, size, origin=(0, 0, 0)):
    """Create and return a 3D tetragonal lattice.

    Parameters
    ----------
    name : str
    hxy : float
        lattice spacing in the xy-plane
    hz : float
        lattice spacing in the z-direction
    size : int[3]
        Number of lattice nodes in each axis direction.
    origin : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    pc = PrimitiveCell.for_tetragonal_lattice(hxy, hz)
    return Lattice(name, pc, size, origin)


def make_body_centered_tetragonal_lattice(name, hxy, hz, size,
                                          origin=(0, 0, 0)):
    """Create and return a 3D body-centered tetragonal lattice.

    Parameters
    ----------
    name : str
    hxy : float
        lattice spacing in the xy-plane
    hz : float
        lattice spacing in the z-direction
    size : int[3]
        Number of lattice nodes in each axis direction.
    origin : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    pc = PrimitiveCell.for_body_centered_tetragonal_lattice(hxy, hz)
    return Lattice(name, pc, size, origin)


def make_hexagonal_lattice(name, hxy, hz, size, origin=(0, 0, 0)):
    """Create and return a 3D hexagonal lattice.

    Parameters
    ----------
    name : str
    hxy : float
        lattice spacing in the xy-plane
    hz : float
        lattice spacing in the z-direction
    size : int[3]
        Number of lattice nodes in each axis direction.
    origin : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    pc = PrimitiveCell.for_hexagonal_lattice(hxy, hz)
    return Lattice(name, pc, size, origin)


def make_orthorhombic_lattice(name, hs, size, origin=(0, 0, 0)):
    """Create and return a 3D orthorhombic lattice.

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
    pc = PrimitiveCell.for_orthorhombic_lattice(hs[0], hs[1], hs[2])
    return Lattice(name, pc, size, origin)


def make_body_centered_orthorhombic_lattice(name, hs, size,
                                            origin=(0, 0, 0)):
    """Create and return a 3D body-centered orthorhombic lattice.

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
    pc = PrimitiveCell.for_body_centered_orthorhombic_lattice(
        hs[0], hs[1], hs[2])
    return Lattice(name, pc, size, origin)


def make_face_centered_orthorhombic_lattice(name, hs, size,
                                            origin=(0, 0, 0)):
    """Create and return a 3D face-centered orthorhombic lattice.

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
    pc = PrimitiveCell.for_face_centered_orthorhombic_lattice(
        hs[0], hs[1], hs[2])
    return Lattice(name, pc, size, origin)


def make_base_centered_orthorhombic_lattice(name, hs, size,
                                            origin=(0, 0, 0)):
    """Create and return a 3D base-centered orthorhombic lattice.

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
    pc = PrimitiveCell.for_base_centered_orthorhombic_lattice(
        hs[0], hs[1], hs[2])
    return Lattice(name, pc, size, origin)


def make_monoclinic_lattice(name, hs, beta, size, origin=(0, 0, 0)):
    """Create and return a 3D monoclinic lattice.

    Parameters
    ----------
    name : str
    hs : float[3]
        lattice spacings in each axis direction
    beta: float
        angle between the (conventional) unit cell edges (in radians),
    size : int[3]
        Number of lattice nodes in each axis direction.
    origin : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    pc = PrimitiveCell.for_monoclinic_lattice(hs[0], hs[1], hs[2], beta)
    return Lattice(name, pc, size, origin)


def make_base_centered_monoclinic_lattice(name, hs, beta, size,
                                          origin=(0, 0, 0)):
    """Create and return a 3D base-centered monoclinic lattice.

    Parameters
    ----------
    name : str
    hs : float
        lattice spacing in each axis direction
    beta: float
        angle between the (conventional) unit cell edges (in radians),
    size : int[3]
        Number of lattice nodes in each axis direction.
    origin : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    pc = PrimitiveCell.for_base_centered_monoclinic_lattice(
        hs[0], hs[1], hs[2], beta)
    return Lattice(name, pc, size, origin)


def make_triclinic_lattice(name, hs, angles, size, origin=(0, 0, 0)):
    """Create and return a 3D triclinic lattice.

    Parameters
    ----------
    name : str
    hs : float[3]
        lattice spacings in each axis direction
    angles : float[3]
        angles between the (conventional) unit cell edges (in radians)
    size : int[3]
        Number of lattice nodes in each axis direction.
    origin : float[3], default value = (0, 0, 0)
        lattice origin

    Returns
    -------
    lattice : Lattice
        A reference to a Lattice object.
    """
    pc = PrimitiveCell.for_triclinic_lattice(
        hs[0], hs[1], hs[2], angles[0], angles[1], angles[2])
    return Lattice(name, pc, size, origin)
