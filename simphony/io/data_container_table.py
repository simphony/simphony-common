import numpy
import tables
from collections import MutableMapping
from itertools import izip

from simphony.io.data_container_description import Data, Mask
from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer


class DataContainerTable(MutableMapping):
    """ A proxy class to an HDF5 group node with serialised DataContainers.

    The class implements the Mutable-Mapping api where each DataContainer
    instance is mapped to the row index in the table.

    """

    @property
    def valid(self):
        return self._table is not None

    def __init__(self, root, name='data_containers'):
        """ Create a proxy object for an HDF5 backed data container table.

        Parameters
        ----------
       root : tables.Group
            The root node where to add the data container table structures.
        name : string
            The name of the new group that will be created.

        """
        # Setup hdf5 nodes
        handle = root._v_file
        try:
            group = getattr(root, name)
        except AttributeError:
            group = handle.create_group(root, name)
        finally:
            self._group = group

        try:
            self._table = group.data
        except AttributeError:
            self._table = handle.create_table(group, 'data', Data)

        try:
            self._mask = group.mask
        except AttributeError:
            self._mask = handle.create_table(group, 'mask', Mask)

        # prepare useful mappings
        columns = Data.columns
        members = CUBA.__members__
        self._cuba_to_position = {
            cuba: columns[member.lower()]._v_pos
            for member, cuba in members.items()}
        self._cuba_to_column = {
            cuba: member.lower()
            for member, cuba in members.items()}
        self._position_to_cuba = {
            columns[member.lower()]._v_pos: cuba
            for member, cuba in members.items()}

    def append(self, data):
        """ Append the data to the end of the table.

        Parameters
        ----------
        data : DataContainer
            The DataContainer instance to save.

        Returns
        -------
        index : integer
            The index position of the saved row.

        """
        table = self._table
        mask = self._mask
        positions = self._cuba_to_position
        columns = self._cuba_to_column
        row = table.row
        mask_row = numpy.zeros(
            shape=mask.coldtypes['mask'].shape, dtype=numpy.bool)
        for key in data:
            row[columns[key]] = data[key]
            mask_row[positions[key]] = True
        row.append()
        table.flush()
        mask.append(mask_row)
        mask.flush()

    def __getitem__(self, row_number):
        """ Return the DataContainer in row.

        """
        cuba = self._position_to_cuba
        row = self._table[row_number]
        mask_row = self._mask[row_number][0]
        return DataContainer({
            cuba[index]: row[index]
            for index, valid in enumerate(mask_row) if valid})

    def __setitem__(self, row_number, data):
        """ Set the data in row from the DataContainer.

        """
        table = self._table
        mask = self._mask
        positions = self._cuba_to_position
        row = [0] * len(positions)
        mask_row = [False] * len(positions)
        for key in data:
            row[positions[key]] = data[key]
            mask_row[positions[key]] = True
        table.modify_rows(start=row_number, rows=[row])
        mask.modify_rows(start=row_number, rows=[(mask_row,)])

    def __delitem__(self, row_number):
        """ Delete the row.

        """
        table = self._table
        if table.nrows == 1 and row_number == 0:
            table.remove()
            self._mask.remove()
            group = self._group
            self._table = tables.Table(group, 'data', Data)
            self._mask = tables.Table(group, 'mask', Mask)
        else:
            self._table.remove_row(row_number)
            self._mask.remove_row(row_number)

    def __len__(self):
        """ The number of rows in the table.

        """
        assert self._table.nrows == self._mask.nrows
        return self._table.nrows

    def itersequence(self, sequence):
        """ Iterate over a sequence of row coordinates.

        """
        assert self._table.nrows == self._mask.nrows
        cuba = self._position_to_cuba
        for row, mask in izip(
                self._table.itersequence(sequence),
                self._mask.itersequence(sequence)):
            mask_row = mask[0]
            yield DataContainer({
                cuba[index]: row[index]
                for index, valid in enumerate(mask_row) if valid})

    def __iter__(self):
        """ Iterate over all the rows
        """
        assert self._table.nrows == self._mask.nrows
        cuba = self._position_to_cuba
        for row, mask in izip(self._table, self._mask):
            mask_row = mask[0]
            yield DataContainer({
                cuba[index]: row[index]
                for index, valid in enumerate(mask_row) if valid})
