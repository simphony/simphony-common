from collections import Sequence

import numpy

from .data_container_description import NoUIDRecord
from .data_conversion import (convert_from_file_type,
                              convert_to_file_type)
from ..core.cuba import CUBA
from ..core.data_container import DataContainer


class IndexedDataContainerTable(Sequence):
    """ A proxy class to an HDF5 group node with serialised DataContainers.

    The class implements the Sequence api where each DataContainer
    instance is mapped to the row. In addition the class implements
    update (i.e. ``__setitem__``) and ``append``.

    """

    @property
    def valid(self):
        return self._table is not None

    def __init__(
            self, root, name='data_containers',
            record=None, expected_number=None):
        """ Create a proxy object for an HDF5 backed data container table.

        Parameters
        ----------
        root : tables.Group
            The root node where to add the data container table structures.
        name : string
            The name of the new group that will be created. Default name is
            'data_containers'
        record : table.IsDescription
            The table columns description to use. Default is to use the
            main data_container record without uid, if a new table needs to
            be created or the already existing record if a table already
            exists in file.

            .. note:: The record is expected to container only


        """
        handle = root._v_file
        self._parent = parent = root

        if hasattr(parent, name):
            self._table = getattr(parent, name)
        else:
            if record is None:
                record = NoUIDRecord
            self._table = handle.create_table(
                parent, name, record, expectedrows=expected_number)

        # Prepare useful mappings
        columns = self._table.cols.data._v_desc._v_colobjects
        members = CUBA.__members__
        self._cuba_to_position = {
            cuba: columns[member.lower()]._v_pos
            for member, cuba in members.items()
            if member.lower() in columns}
        self._position_to_cuba = {
            columns[member.lower()]._v_pos: cuba
            for member, cuba in members.items()
            if member.lower() in columns}

    def append(self, data):
        """ Append the data to the end of the table.

        Parameters
        ----------
        data : DataContainer
            The DataContainer instance to save.

        Returns
        -------
        index : int
            The index of the saved row.

        """
        table = self._table
        row = table.row
        self._populate_row(row, data)
        row.append()
        table.flush()
        return table.nrows - 1

    def __getitem__(self, index):
        """ Return the DataContainer in index.

        """
        row = self._table[index]
        return self._retrieve(row)

    def __setitem__(self, index, data):
        """ Update the data in index.

        """
        table = self._table
        if 0 <= index < table.nrows:
            row = self._create_rec_array(data)
            table[index] = tuple(row)
        else:
            raise IndexError('Index {} out of bounds'.format(index))

    def __iter__(self):
        """ Iterate over all the rows

        """
        for row in self._table:
            yield self._retrieve(row)

    def __len__(self):
        """ The number of rows in the table.

        """
        return self._table.nrows

    def _populate_row(self, row, value):
        """ Populate the row from the DataContainer.

        """
        positions = self._cuba_to_position
        mask = numpy.zeros(
            shape=self._table.coldtypes['mask'].shape, dtype=numpy.bool)
        data = list(row['data'])
        for key in value:
            if key in positions:
                data[positions[key]] = convert_to_file_type(value[key], key)
                mask[positions[key]] = True

        row['mask'] = mask
        row['data'] = tuple(data)

    def _create_rec_array(self, value):
        """ Create a rec_array row from a DataContainer

        """
        positions = self._cuba_to_position
        rec_array = numpy.zeros(shape=1, dtype=self._table._v_dtype)[0]
        data = rec_array['data']
        mask = rec_array['mask']
        for key in value:
            if key in positions:
                position = positions[key]
                # special case array valued cuba keys
                # see numpy issue https://github.com/numpy/numpy/issues/3126
                if numpy.isscalar(data[position]):
                    data[position] = convert_to_file_type(value[key], key)
                else:
                    data[position][:] = convert_from_file_type(value[key], key)
                mask[position] = True
        return rec_array

    def _retrieve(self, row):
        """ Return the DataContainer from a table row instance.

        """
        cuba = self._position_to_cuba
        mask = row['mask']
        data = row['data']
        return DataContainer({
            cuba[index]: convert_from_file_type(data[index], cuba[index])
            for index, valid in enumerate(mask) if valid})
