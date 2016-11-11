from ..cuds import ABCLattice, LatticeNode
from ..cuds.primitive_cell import PrimitiveCell, BravaisLattice
from .indexed_data_container_table import IndexedDataContainerTable
from .data_container_description import NoUIDRecord
from ..core.data_container import DataContainer
from ..core import CUBA

import numpy as np


LATTICE_CUDS_VERSION = 2


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
        attrs = group.lattice.attrs
        self._primitive_cell = PrimitiveCell(
            attrs.primitive_cell[0], attrs.primitive_cell[1],
            attrs.primitive_cell[2], BravaisLattice(attrs.bravais_lattice))

        self._size = attrs.size
        self._origin = attrs.origin

        self._table = IndexedDataContainerTable(group, 'lattice')
        self._data = IndexedDataContainerTable(group, 'data')

        self._items_count = {CUBA.NODE: lambda: self._table}

    @classmethod
    def create_new(cls, group, primitive_cell, size, origin, record=None):
        """ Create a new lattice in H5CUDS file.

        Parameters
        ----------
        group : HDF5 group in PyTables file
            reference to a group (folder) in PyTables file where the tables
            for lattice and data will be located
        primitive_cell : PrimitiveCell
            primitive cell specifying the 3D Bravais lattice
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

        pc = primitive_cell
        lattice._table.attrs.primitive_cell = [pc.p1, pc.p2, pc.p3]
        lattice._table.attrs.bravais_lattice = pc.bravais_lattice
        lattice._table.attrs.size = size
        lattice._table.attrs.origin = origin

        IndexedDataContainerTable(group, 'data', NoUIDRecord, 1)

        return cls(group)

    def count_of(self, item_type):
        """ Return the count of item_type in the container.

        Parameters
        ----------
        item_type : CUBA
            The CUBA enum of the type of the items to return the count of.

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

    # Private

    def _get_node(self, index):
        """ Get a copy of the node corresponding to the given index.

        Parameters
        ----------
        index : int[3]
            node index coordinate

        Returns
        -------
        node : LatticeNode

        """
        try:
            n = np.ravel_multi_index(index, self._size)
        except ValueError:
            raise IndexError('invalid index: {}'.format(index))
        return LatticeNode(index, self._table[n])

    def _update_nodes(self, nodes):
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

    def _iter_nodes(self, indices=None):
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
