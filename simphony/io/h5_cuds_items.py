import abc
from collections import MutableMapping

import tables

from .data_container_table import DataContainerTable


class H5CUDSItems(MutableMapping):
    """ A proxy class to an HDF5 group node with serialised CUDS items.

    The class implements the Mutable-Mapping api where each item instance
    is mapped to uuid.

    """

    @property
    def valid(self):
        """ A PyTables table is opened/created and the object is valid.

        """
        return getattr(self, '_items', None) is not None

    def __init__(self, root, record, name='items'):
        """ Create a proxy object for an HDF5 backed items container.

        Parameters
        ----------
        root : tables.Group
            The root node where to add the items and data table structures.
        name : string
            The name of the new group that will be created. Default name is
            'items'.

        """
        if hasattr(root, name):
            self._group = getattr(root, name)
            self._items = self._group.items
        else:
            handle = root._v_file
            self._group = handle.create_group(root, name)
            self._items = handle.create_table(self._group, 'items', record)
        self._data = DataContainerTable(self._group, name='data')

    def __getitem__(self, uid):
        """ Return the Particle with the provided id.

        """
        for row in self._items.where(
                'uid == value',  condvars={'value': uid.hex}):
            return self._retrieve(row)
        else:
            raise KeyError(
                'Record (id={id}) does not exist'.format(id=uid))

    def __setitem__(self, uid, item):
        """ Set the particle in row with item.

        - If the uid does not exist in the Table a new row will be appended.
        - If the ``item.uid`` is ``None`` then ``item.uid = uid``.


        """
        if not hasattr(uid, 'hex'):
            raise KeyError('{} is not a uuid.UUID'.format(uid))

        if item.uid is None:
            item.uid = uid

        table = self._items
        for row in table.where(
                'uid == value', condvars={'value': uid.hex}):
            self._populate(row, item)
            row.update()
            # see https://github.com/PyTables/PyTables/issues/11
            row._flush_mod_rows()
            return
        else:
            row = table.row
            row['uid'] = uid.hex
            self._populate(row, item)
            row.append()
            table.flush()

    def __delitem__(self, uid):
        """ Delete the row.

        """
        if not hasattr(uid, 'hex'):
            raise KeyError('{} is not a uuid.UUID'.format(uid))

        table = self._items
        for row in table.where(
                'uid == value', condvars={'value': uid.hex}):
            if table.nrows == 1:
                record = table.description
                # pytables due to hdf5 limitations does
                # not support removing the last row of table
                # so we delete the table and
                # create new empty table in this situation
                table.remove()
                self._items = tables.Table(self._group, 'items', record)
                del self._data[uid]
            else:
                table.remove_row(row.nrow)
            break
        else:
            raise KeyError(
                'Record (id={id}) does not exist'.format(id=uid))

    def __len__(self):
        """ The number of rows in the table.

        A runtime error is raised when the number of rows in the items and data
        tables is not equal.

        """
        nrows = self._items.nrows
        if len(self._data) != nrows:
            message = (
                "internal items and data tables contain different number of "
                "items:{} != {}")
            raise RuntimeError(message.format(nrows, len(self._data)))
        return nrows

    def itersequence(self, sequence):
        """ Iterate over a sequence of row ids.

        """
        for uid in sequence:
            yield self[uid]

    def __iter__(self):
        """ Iterate over all the rows

        """
        for row in self._items:
            yield self._retrieve(row)

    def __contains__(self, uid):
        for row in self._items.where(
                'uid == value', condvars={'value': uid.hex}):
            return True
        else:
            return False

    def add_unsafe(self, item):
        """ Add item without checking for a unique uid.

        .. note::
          The item is expected to already have a uid set.

        """
        table = self._items
        row = table.row
        row['uid'] = item.uid.hex
        self._populate(row, item)
        row.append()
        table.flush()

    def add_safe(self, item):
        """ Add item while checking for a unique uid.

        .. note::
          The item is expected to already have a uid set.

        """
        uid = item.uid
        table = self._items
        for row in table.where(
                'uid == value', condvars={'value': uid.hex}):
            raise ValueError(
                'Record (id={id}) already exists'.format(id=uid))
        else:
            self.add_unsafe(item)

    def update_existing(self, item):
        """ Update an item if it already exists.
        """
        uid = item.uid
        if not hasattr(uid, 'hex'):
            raise ValueError('{} is not a uuid.UUID'.format(uid))
        table = self._items
        for row in table.where(
                'uid == value', condvars={'value': uid.hex}):
            self._populate(row, item)
            row.update()
            # see https://github.com/PyTables/PyTables/issues/11
            row._flush_mod_rows()
            return
        else:
            message = 'Item with id {} does not exist'
            raise ValueError(message.format(uid))

    @abc.abstractmethod
    def _populate(self, row, item):
        """ Populate the row from the item.

        """

    @abc.abstractmethod
    def _retrieve(self, row):
        """ Return the item instance from a table row instance.

        """
