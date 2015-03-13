from simphony.cuds.lattice import ABCLattice
from simphony.cuds.lattice import LatticeNode
from simphony.io.indexed_data_container_table import IndexedDataContainerTable
from simphony.io.data_container_description import NoUIDRecord
from simphony.core.data_container import DataContainer

import numpy as np


class FileLattice(ABCLattice):
    """
    FileLattice object to use in file lattices.

    Attributes
    ----------
    file : PyTables file
        reference to PyTables file where the lattice is or will be located
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

    Returns:
    ----------
    FileLattice
        The lattice newly added to the file or existing in the file.

    """
    def __init__(self, file, name, type=None, base_vect=None,
                 size=None, origin=None, record=None):

        self._file = file
        self._name = name
        self._group = file.root.lattice

        # If Lattice not in file, create a lattice
        if self._name not in self._file.root.lattice:
            if type is None:
                error_str = ("Lattice '{}' does not exist in file. "
                             "Type, base_vect, size and origin must "
                             "be given proper values.")
                raise ValueError(error_str.format(name))
            # Set FileLattice attributes
            self._type = type
            self._base_vect = np.array(base_vect, dtype=np.float)
            self._size = tuple(size)
            self._origin = np.array(origin, dtype=np.float)
            self._record = record

            # If record not specified use NoUIDRecord
            if self._record is None:
                self._record = NoUIDRecord
            self._table = IndexedDataContainerTable(
                self._group, name, self._record, np.prod(self._size))
            for i in xrange(np.prod(self._size)):
                self._table.append(DataContainer())

            # Set table attributes
            lattice = self._group._f_getChild(self.name)
            lattice.attrs.type = self._type
            lattice.attrs.base_vect = self._base_vect
            lattice.attrs.size = self._size
            lattice.attrs.origin = self._origin

        # If Lattice already in file, return a reference
        else:
            self._table = IndexedDataContainerTable(self._group, name)
            lattice = self._group._f_getChild(self.name)
            self._type = lattice.attrs.type
            self._base_vect = lattice.attrs.base_vect
            self._size = lattice.attrs.size
            self._origin = lattice.attrs.origin

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
