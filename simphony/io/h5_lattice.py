from simphony.cuds.lattice import ABCLattice
from simphony.cuds.lattice import LatticeNode
from simphony.io.indexed_data_container_table import IndexedDataContainerTable
from simphony.io.data_container_description import NoUIDRecord
from simphony.core.data_container import DataContainer

import numpy as np


class H5Lattice(ABCLattice):
    """ H5Lattice object to use H5CUDS lattices.

    """
    def __init__(self, group, name):
        """ Return a reference to existing lattice in a H5CUDS lattice group

        Parameters
        ----------
        group : HDF5 group in PyTables file
            reference to a group (folder) in PyTables file where the lattice is
            located
        name : str
            name of the lattice

        """
        self._group = group
        self._name = name
        self._table = IndexedDataContainerTable(self._group, name)

        lat = self._group._f_getChild(self.name)
        self._type = lat.attrs.type
        self._base_vect = lat.attrs.base_vect
        self._size = lat.attrs.size
        self._origin = lat.attrs.origin

    @classmethod
    def create_new(cls, group, name, type, base_vect, size, origin,
                   record=None):
        """
        Parameters
        ----------
        group : HDF5 group in PyTables file
            reference to a group (folder) in PyTables file where the lattice
            will be located
        name : str
            name of the lattice
        type : string
            Bravais lattice type (should agree with the _base_vect below).
        base_vect : D x float
            defines a Bravais lattice (an alternative for primitive vectors).
        size : D x size
            number of lattice nodes (in the direction of each axis).
        origin : D x float
            origin of lattice
        record : tables.IsDescription
            A class that describes column types for PyTables table.

        """
        # If record not specified use NoUIDRecord in table initialization
        table = IndexedDataContainerTable(group, name,
            record if record is not None else NoUIDRecord, np.prod(size))

        for i in xrange(np.prod(size)):
            table.append(DataContainer())

        # Set table attributes
        lattice = group._f_getChild(name)
        lattice.attrs.type = type
        lattice.attrs.base_vect = base_vect
        lattice.attrs.size = size
        lattice.attrs.origin = origin

        return cls(group, name)

    def get_node(self, index):
        """Get a copy of the node corresponding to the given index.

        Parameters:
        -----------
        index : tuple of D x int (node index coordinate)

        Returns:
        -----------
        A reference to a LatticeNode object

        """
        n = np.ravel_multi_index(index, self._size)
        return LatticeNode(index, self._table[n])

    def update_node(self, node):
        """ Updates FileLattice data for a LatticeNode

        Parameters:
            node : LatticeNode
                reference to LatticeNode object

        """
        # Find correct row for node
        n = np.ravel_multi_index(node.index, self._size)
        self._table[n] = node.data

    def iter_nodes(self, indices=None):
        """Get an iterator over the LatticeNodes described by the ids.

        Parameters:
        -----------
        indices : iterable set of D x int, optional
            node index coordinates

        Returns:
        -----------
        A generator for LatticeNode objects

        """
        if indices is None:
            for row_number, data in enumerate(self._table):
                index = np.unravel_index(row_number, self._size)
                yield LatticeNode(index, data)
        else:
            for index in indices:
                yield self.get_node(index)

    def get_coordinate(self, index):
        """Get coordinate of the given index coordinate.

        Parameters:
        -----------
        index : D x int (node index coordinate)

        Returns:
        -----------
        D x float

        """
        if self._type == 'Hexagonal':
            raise NotImplementedError("""Get_coordinate for
                Hexagonal system not implemented!""")

        return self._origin + self._base_vect*np.array(index)

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
    def name(self):
        return self._table._table._v_name

    @name.setter
    def name(self, value):
        self._table._table._f_rename(value)
