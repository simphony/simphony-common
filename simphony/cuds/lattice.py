"""Lattice data specification of SimPhoNy CUDS, a non-wrapper implementation.

Classes:
--------
LatticeNode:
    represents a single node of a lattice. Stores the node index coordinate
    (used as the node id) and node related data in a data container.

Lattice:
    describes a Bravais lattice. Stores references to lattice nodes.
    References stored only on demand (i.e. default references are to None)

Routines:
---------
make_hexagonal_lattice:
    create and return a 2D hexagonal lattice.

make_square_lattice:
    create and return a 2D square lattice.

make_rectangular_lattice:
    create and return a 2D rectangular lattice.

make_cubic_lattice:
    create and return a 3D cubic lattice.

make_orthorombicp_lattice:
    create and return a 3D orthorhombic (primitive) lattice.
"""
# ===========================================================================
# Import modules
# ===========================================================================
import copy
import numpy as np
from math import sqrt
import simphony.core.data_container as dc


# ===========================================================================
# class LatticeNode
# ===========================================================================
class LatticeNode:
    """
    A single node of a lattice.

    Parameters:
    -----------
    id: tuple of D x int
        node index coordinate
    lat_node: reference to a LatticeNode object
        data copied from the given node
    """
    def __init__(self, id, lat_node=None):
        self.id = tuple(id)
        self.data = dc.DataContainer()

        if lat_node is not None:
            self.copy_data(lat_node)
        # end if

    # -----------------------------------------------------------------------
    def copy_data(self, lat_node):
        """Copy data from the given node.

        Parameters:
        -----------
        lat_node: reference to a LatticeNode object
        """
        if lat_node is None:
            return
        # end if

        for key in lat_node.data:
            self.data[key] = copy.deepcopy(lat_node.data[key])
        # end for

    # -----------------------------------------------------------------------
# end


# ===========================================================================
# class Lattice
# ===========================================================================
class Lattice:
    """
    A Bravais lattice; stores references to LatticeNodes.

    Parameters:
    -----------
    name: string
    type: string
        Bravais lattice type (should agree with the base_vect below).
    base_vect: D x float
        defines a Bravais lattice (an alternative for primitive vectors).
    size: D x size
        number of lattice nodes (in the direction of each axis).
    origin: D x float
    """
    def __init__(self, name, type, base_vect, size, origin):
        self.name = name
        self.type = type
        self.base_vect = np.array(base_vect, dtype=np.float)
        self.size = np.array(size, dtype=np.uint32)
        self.origin = np.array(origin, dtype=np.float)
        self.lat_nodes = np.empty(size, dtype=object)

    # -----------------------------------------------------------------------
    def get_node(self, id):
        """Get a copy of the node corresponding to the given id.

        Parameters:
        -----------
        id: tuple of D x int (node index coordinate)

        Returns:
        -----------
        A reference to a LatticeNode object
        """
        tuple_id = tuple(id)
        return LatticeNode(tuple_id, self.lat_nodes[tuple_id])

    # -----------------------------------------------------------------------
    def update_node(self, lat_node):
        """Update the corresponding lattice node (data copied).

        Parameters:
        -----------
        lat_node: reference to a LatticeNode object
            data copied from the given node
        """
        id = lat_node.id
        if self.lat_nodes[id] is None:
            self.lat_nodes[id] = LatticeNode(id, lat_node)
        else:
            self.lat_nodes[id].copy_data(lat_node)

    # -----------------------------------------------------------------------
    def iter_nodes(self, ids=None):
        """Get an iterator over the LatticeNodes described by the ids.

        Parameters:
        -----------
        ids: iterable set of D x int (node index coordinates)

        Returns:
        -----------
        A generator for LatticeNode objects
        """
        if ids is None:
            for id, val in np.ndenumerate(self.lat_nodes):
                yield self.get_node(id)
        else:
            for id in ids:
                yield self.get_node(id)
        # end if else

    # -----------------------------------------------------------------------
    def get_coordinate(self, id):
        """Get coordinate of the given index coordinate.

        Parameters:
        -----------
        id: D x int (node index coordinate)

        Returns:
        -----------
        D x float
        """
        return self.origin + self.base_vect*np.array(id)

# end


# ===========================================================================
# Functions for creating Bravais lattices
# ===========================================================================
def make_hexagonal_lattice(name, h, size, origin=(0, 0)):
    """Create and return a 2D hexagonal lattice.

    Parameters:
    -----------
    name: string
    h: float
        lattice spacing.
    size: 2 x int
        number of lattice nodes (in each axis direction).
    origin: 2 x float (default value = (0,0))
        lattice origin.

    Returns:
    -----------
    A reference to a Lattice object.
    """
    return Lattice(name, 'Hexagonal', (0.5*h, 0.5*sqrt(3)*h), size, origin)


# ---------------------------------------------------------------------------
def make_square_lattice(name, h, size, origin=(0, 0)):
    """Create and return a 2D square lattice.

    Parameters:
    -----------
    name: string
    h: float
        lattice spacing.
    size: 2 x int
        number of lattice nodes (in each axis direction).
    origin: 2 x float (default value = (0,0))
        lattice origin.

    Returns:
    -----------
    A reference to a Lattice object.
    """
    return Lattice(name, 'Square', (h, h), size, origin)


# ---------------------------------------------------------------------------
def make_rectangular_lattice(name, hs, size, origin=(0, 0)):
    """Create and return a 2D rectangular lattice.

    Parameters:
    -----------
    name: string
    hs: 2 x float
        lattice spacings (in each axis direction).
    size: 2 x int
        number of lattice nodes (in each axis direction).
    origin: 2 x float (default value = (0,0))
        lattice origin.

    Returns:
    -----------
    A reference to a Lattice object.
    """
    return Lattice(name, 'Rectangular', hs, size, origin)


# ---------------------------------------------------------------------------
def make_cubic_lattice(name, h, size, origin=(0, 0, 0)):
    """Create and return a 3D cubic lattice.

    Parameters:
    -----------
    name: string
    h: float
        lattice spacing.
    size: 3 x int
        number of lattice nodes (in each axis direction).
    origin: 3 x float (default value = (0,0,0))
        lattice origin.

    Returns:
    -----------
    A reference to a Lattice object.
    """
    return Lattice(name, 'Cubic', (h, h, h), size, origin)


# ---------------------------------------------------------------------------
def make_orthorombicp_lattice(name, hs, size, origin=(0, 0, 0)):
    """Create and return a 3D orthorombic primitive lattice.

    Parameters:
    -----------
    name: string
    hs: 3 x float
        lattice spacings (in each axis direction).
    size: 3 x int
        number of lattice nodes (in each axis direction).
    origin: 3 x float (default value = (0,0,0))
        lattice origin.

    Returns:
    -----------
    A reference to a Lattice object.
    """
    return Lattice(name, 'OrthorombicP', hs, size, origin)
# ===========================================================================
# Keijo Mattila & Tuomas Puurtinen, SimPhoNy, JYU, 2014.
# ===========================================================================
