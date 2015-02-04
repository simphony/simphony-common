from collections import MutableSequence

import numpy

from simphony.io.data_container_description import NoUIDRecord
from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer


class IndexedDataContainerTable(MutableSequence):
    """ A proxy class to an HDF5 group node with serialised DataContainers.

    The class implements the MutableSequence api where each DataContainer
    instance is mapped to the row without support of __delitem__.

    """

    @property
    def valid(self):
        return self._table is not None

    def __init__(self, root, name='data_containers', record=None):
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
            self._table = handle.create_table(parent, name, record)

        # Prepare useful mappings
        columns = self._table.cols.Data._v_desc._v_colobjects
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
        self._populate(row, data)
        row.append()
        table.flush()
        return table.nrows

    def __getitem__(self, index):
        """ Return the DataContainer in index.

        """
        row = self._table[index]
        return self._retrieve(row)

    def __delitem__(self, index):
        raise NotImplementedError()

    def __setitem__(self, index, data):
        """ Update the data in index.

        """
        row = self._table[index]
        self._populate(row, data)
        row.update()
        # see https://github.com/PyTables/PyTables/issues/11
        row._flush_mod_rows()

    def __len__(self):
        """ The number of rows in the table.

        """
        return self._table.nrows

    def _populate(self, row, value):
        """ Populate the row from the DataContainer.

        """
        positions = self._cuba_to_position
        mask = numpy.zeros(
            shape=self._table.coldtypes['mask'].shape, dtype=numpy.bool)
        data = list(row['Data'])
        for key in value:
            if key in positions:
                data[positions[key]] = value[key]
                mask[positions[key]] = True
        row['mask'] = mask
        row['Data'] = tuple(data)

    def _retrieve(self, row):
        """ Return the DataContainer from a table row instance.

        """
        cuba = self._position_to_cuba
        mask = row['mask']
        data = row['Data']
        return DataContainer({
            cuba[index]: data[index]
            for index, valid in enumerate(mask) if valid})
