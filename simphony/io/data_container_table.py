from collections import MutableMapping
import uuid

import numpy
import tables

from simphony.io.data_container_description import Record
from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer


class DataContainerTable(MutableMapping):
    """ A proxy class to an HDF5 group node with serialised DataContainers.

    The class implements the Mutable-Mapping api where each DataContainer
    instance is mapped to uuid.


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
        handle = root._v_file
        self._parent = parent = root

        if hasattr(parent, name):
            self._table = getattr(parent, name)
        else:
            self._table = handle.create_table(parent, name, Record)

        # prepare useful mappings
        columns = Record.columns['Data']._v_colobjects
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
        uid : uuid.UUID
            The index of the saved row.

        """
        table = self._table
        positions = self._cuba_to_position
        row = table.row
        mask = numpy.zeros(
            shape=table.coldtypes['mask'].shape, dtype=numpy.bool)
        uid = uuid.uuid4()
        row['index'] = uid.bytes
        data_row = list(row['Data'])
        for key in data:
            data_row[positions[key]] = data[key]
            mask[positions[key]] = True
        row['mask'] = mask
        row['Data'] = tuple(data_row)
        row.append()
        table.flush()
        return uid

    def __getitem__(self, uid):
        """ Return the DataContainer in row.

        """
        cuba = self._position_to_cuba
        for row in self._table.where(
                'index == value',  condvars={'value': uid.bytes}):
            mask = row['mask']
            data = row['Data']
            return DataContainer({
                cuba[index]: data[index]
                for index, valid in enumerate(mask) if valid})

    def __setitem__(self, uid, data):
        """ Set the data in row from the DataContainer.

        """
        table = self._table
        positions = self._cuba_to_position
        for row in table.where(
                'index == value', condvars={'value': uid.bytes}):
            mask = numpy.zeros(
                shape=table.coldtypes['mask'].shape, dtype=numpy.bool)
            data_row = list(row['Data'])
            for key in data:
                data_row[positions[key]] = data[key]
                mask[positions[key]] = True
            row['mask'] = mask
            row['Data'] = tuple(data_row)
            row.update()
            # see https://github.com/PyTables/PyTables/issues/11
            row._flush_mod_rows()
            break
        else:
            raise KeyError('Index {} is not found'.format(uid))

    def __delitem__(self, uid):
        """ Delete the row.

        """
        table = self._table
        for row in table.where(
                'index == value', condvars={'value': uid.bytes}):
            print row
            if table.nrows == 1:
                name = table._v_name
                # pytables due to hdf5 limitations does
                # not support removing the last row of table
                # so we delete the table and
                # create new empty table in this situation
                table.remove()
                parent = self._parent
                self._table = tables.Table(parent, name, Record)
            else:
                table.remove_row(row.nrow)
            break
        else:
            raise ValueError(
                'Record (id={id}) does not exist'.format(id=uid))

    def __len__(self):
        """ The number of rows in the table.

        """
        return self._table.nrows

    def itersequence(self, sequence):
        """ Iterate over a sequence of row ids.

        """
        for uid in sequence:
            yield self.__getitem__(uid)

    def __iter__(self):
        """ Iterate over all the rows
        """
        cuba = self._position_to_cuba
        for row in self._table:
            mask = row['mask']
            data = row['Data']
            yield DataContainer({
                cuba[index]: data[index]
                for index, valid in enumerate(mask) if valid})
