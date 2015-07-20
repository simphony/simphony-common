from simphony.cuds import ABCLattice, LatticeNode
from simphony.io.indexed_data_container_table import IndexedDataContainerTable
from simphony.io.data_container_description import NoUIDRecord
from simphony.core.data_container import DataContainer
from simphony.core.cuds_item import CUDSItem

import numpy as np


LATTICE_CUDS_VERSION = 1


class H5Lattice(ABCLattice):
    """ H5Lattice object to use H5CUDS lattices.

    """
    def __init__(self, group):
        """ Return a reference to existing lattice in a H5CUDS group.

        Parameters
        ----------
        group : HDF5 group in PyTables file
            reference to a group (folder) in PyTables file where the tables
            for lattice and data are located

        """
        if group._v_attrs.cuds_version != LATTICE_CUDS_VERSION:
            raise ValueError("Lattice file layout has an incompatible version")

        self._group = group
        self._type = group.lattice.attrs.type
        self._base_vect = group.lattice.attrs.base_vect
        self._size = group.lattice.attrs.size
        self._origin = group.lattice.attrs.origin

        self._table = IndexedDataContainerTable(group, 'lattice')
        self._data = IndexedDataContainerTable(group, 'data')

        self._items_count = {
            CUDSItem.NODE: lambda: self._table
        }

    @classmethod
    def create_new(cls, group, type, base_vect, size, origin, record=None):
        """ Create a new lattice in H5CUDS file.

        Parameters
        ----------
        group : HDF5 group in PyTables file
            reference to a group (folder) in PyTables file where the tables
            for lattice and data will be located
        type : str
            Bravais lattice type (should agree with the _base_vect below).
        base_vect : float[3]
            defines a Bravais lattice (an alternative for primitive vectors).
        size : int[3]
            number of lattice nodes (in the direction of each axis).
        origin : float[3]
            origin of lattice
        record : tables.IsDescription
            A class that describes column types for PyTables table.

        """
        group._v_attrs.cuds_version = LATTICE_CUDS_VERSION

        # If record not specified use NoUIDRecord in table initialization
        lattice = IndexedDataContainerTable(group, 'lattice',
                                            record if record is not None
                                            else NoUIDRecord, np.prod(size))
        for i in xrange(np.prod(size)):
            lattice.append(DataContainer())

        lattice._table.attrs.type = type
        lattice._table.attrs.base_vect = base_vect
        lattice._table.attrs.size = tuple(size)
        lattice._table.attrs.origin = origin

        IndexedDataContainerTable(group, 'data', NoUIDRecord, 1)

        return cls(group)

    def get_node(self, index):
        """ Get a copy of the node corresponding to the given index.

        Parameters
        ----------
        index : int[3]
            node index coordinate

        Returns
        -------
        A reference to a LatticeNode object

        """
        try:
            n = np.ravel_multi_index(index, self._size)
        except ValueError:
            raise IndexError('invalid index: {}'.format(index))
        return LatticeNode(index, self._table[n])

    def update_nodes(self, nodes):
        """ Updates H5Lattice data for a LatticeNode

        Parameters
        ----------
        nodes : iterable of LatticeNode objects
            reference to LatticeNode objects

        """
        # Find correct row for node
        for node in nodes:
            index = node.index
            try:
                n = np.ravel_multi_index(index, self._size)
            except ValueError:
                raise IndexError('invalid index: {}'.format(index))
            self._table[n] = node.data

    def iter_nodes(self, indices=None):
        """ Get an iterator over the LatticeNodes described by the ids.

        Parameters
        ----------
        indices : iterable set of int[3], optional
            node index coordinates

        Returns
        -------
        A generator for LatticeNode objects

        """
        if indices is None:
            for row_number, data in enumerate(self._table):
                index = np.unravel_index(row_number, self._size)
                yield LatticeNode(index, data)
        else:
            for index in indices:
                yield self.get_node(index)

    def count_of(self, item_type):
        """ Return the count of item_type in the container.

        Parameter
        ---------
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
            return len(self._items_count[item_type]())
        except KeyError:
            error_str = "Trying to obtain count a of non-supported item: {}"
            raise ValueError(error_str.format(item_type))

    def get_coordinate(self, index):
        """ Get coordinate of the given index coordinate.

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
    def name(self):
        return self._group._v_name

    @name.setter
    def name(self, value):
        self._group._f_rename(value)

    @property
    def data(self):
        if len(self._data) == 1:
            return self._data[0]
        else:
            return DataContainer()

    @data.setter
    def data(self, value):
        if len(self._data) == 0:
            self._data.append(value)
        else:
            self._data[0] = value
