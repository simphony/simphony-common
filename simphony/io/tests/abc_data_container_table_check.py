import tempfile
import shutil
import os
import random
import uuid
import abc
from contextlib import closing, contextmanager

import tables
import numpy
from numpy.testing import assert_equal

from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer
from simphony.io.data_container_description import Record
from simphony.io.data_container_table import DataContainerTable


def create_data_container(restrict=None):
    """ Create a data container while respecting the expected data types.

    """

    if restrict is None:
        restrict = CUBA
    data = {cuba: dummy_cuba_value(cuba) for cuba in restrict}
    return DataContainer(data)


def dummy_cuba_value(cuba):
    Data = Record.columns['Data']
    column = CUBA(cuba).name.lower()
    # get the column type
    try:
        column_type = Data.columns[column]
    except AttributeError:
        column_type = Data._v_colobjects[column]

    if numpy.issubdtype(column_type, str):
        value = column.upper()
    elif numpy.issubdtype(column_type, numpy.float):
        value = float(cuba + 3)
    elif numpy.issubdtype(column_type, numpy.integer):
        value = int(cuba + 3)
    else:
        shape = column_type.shape
        if column_type.kind == 'float':
            value = numpy.ones(
                shape=shape, dtype=numpy.float64) * cuba + 3
        elif column_type.kind == 'int':
            value = numpy.ones(
                shape=shape, dtype=numpy.int32) * cuba + 3
        else:
            raise RuntimeError(
                'cannot create value for {}'.format(column_type))
    return value


class ABCDataContainerTableCheck(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def record(self):
        """ The columns configuration that the table is using """

    @property
    def saved_keys(self):
        """ Return the CUBA keys that are actually stored to be saved.

        The default implementation will return the full CUBA keys.

        """
        members = {
            member.lower(): cuba
            for member, cuba in CUBA.__members__.iteritems()}
        data_record = self.record.columns['Data']
        try:
            return [members[column] for column in data_record._v_names]
        except AttributeError:
            return [members[column] for column in data_record.columns]

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, '_test_file.cuds')
        self.maxDiff = None

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    @contextmanager
    def new_table(self, table_name):
        handle = None
        try:
            handle = tables.open_file(self.filename, mode='w')
            root = handle.root
            table = DataContainerTable(root, table_name, record=self.record)
            self.assertEqual(len(table), 0)
            yield table
        finally:
            if handle is not None:
                handle.close()

    @contextmanager
    def open_table(self, table_name, mode='r'):
        handle = None
        try:
            handle = tables.open_file(self.filename, mode=mode)
            root = handle.root
            table = DataContainerTable(root, table_name, record=self.record)
            yield table
        finally:
            if handle is not None:
                handle.close()

    def test_creating_a_data_container_table(self):
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(
                root, 'my_data_table', record=self.record)
            self.assertEqual(len(table), 0)
            self.assertIn('my_data_table', root)
            self.assertTrue(table.valid)
            data_column = root.my_data_table.colinstances['Data']
            expected_column_names = [
                key.name.lower() for key in self.saved_keys]
            self.assertItemsEqual(
                data_column._v_colnames, expected_column_names)

    def test_append_data(self):
        data = create_data_container(restrict=self.saved_keys)
        with self.new_table('my_data_table') as table:
            table.append(data)
        with self.open_table('my_data_table') as table:
            self.assertEqual(len(table), 1)

    def test_set_data(self):
        data = create_data_container(restrict=self.saved_keys)
        with self.new_table('my_data_table') as table:
            uid = uuid.uuid4()
            table[uid] = data
        with self.open_table('my_data_table') as table:
            self.assertEqual(len(table), 1)
            self.assertIn(uid, table)

    def test_append_data_with_missing_keywords(self):
        keys = self.saved_keys[:-1]
        data = create_data_container(restrict=keys)
        with self.new_table('my_data_table') as table:
            table.append(data)
            self.assertEqual(len(table), 1)
            uid = table.append(data)
            self.assertEqual(len(table), 2)
        with self.open_table('my_data_table') as table:
            self.assertEqual(len(table), 2)
            loaded_data = table[uid]
            expected = create_data_container(restrict=keys)
            self.assertDataContainersEqual(loaded_data, expected)

    def test_set_data_with_missing_keywords(self):
        keys = self.saved_keys[:-1]
        data = create_data_container(restrict=keys)
        with self.new_table('my_data_table') as table:
            table[uuid.uuid4()] = data
            self.assertEqual(len(table), 1)
            uid = uuid.uuid4()
            table[uid] = data
            self.assertEqual(len(table), 2)
        with self.open_table('my_data_table') as table:
            self.assertEqual(len(table), 2)
            loaded_data = table[uid]
            expected = create_data_container(restrict=keys)
            self.assertDataContainersEqual(loaded_data, expected)

    def test_append_data_with_more_keywords(self):
        data = create_data_container()
        with self.new_table('my_data_table') as table:
            table.append(data)
            self.assertEqual(len(table), 1)
            uid = table.append(data)
            self.assertEqual(len(table), 2)
        with self.open_table('my_data_table') as table:
            self.assertEqual(len(table), 2)
            loaded_data = table[uid]
            expected = create_data_container(restrict=self.saved_keys)
            self.assertDataContainersEqual(loaded_data, expected)

    def test_set_data_with_more_keywords(self):
        data = create_data_container()
        with self.new_table('my_data_table') as table:
            table[uuid.uuid4()] = data
            self.assertEqual(len(table), 1)
            uid = uuid.uuid4()
            table[uid] = data
            self.assertEqual(len(table), 2)
        with self.open_table('my_data_table') as table:
            self.assertEqual(len(table), 2)
            loaded_data = table[uid]
            expected = create_data_container(restrict=self.saved_keys)
            self.assertDataContainersEqual(loaded_data, expected)

    def test_get_data(self):
        saved_keys = self.saved_keys
        data = create_data_container(restrict=saved_keys)
        data1 = DataContainer(data)
        key = saved_keys[0]
        data[key] = dummy_cuba_value(key) + dummy_cuba_value(key)
        with self.new_table('my_data_table') as table:
            uid = table.append(data)
            uid1 = uuid.uuid4()
            table[uid1] = data1
        with self.open_table('my_data_table') as table:
            self.assertEqual(len(table), 2)
            self.assertDataContainersEqual(table[uid], data)
            self.assertDataContainersEqual(table[uid1], data1)

    def test_get_data_with_missing_keywords(self):
        saved_keys = self.saved_keys
        data = create_data_container(restrict=saved_keys)
        data1 = create_data_container(restrict=saved_keys[:-1])
        key = saved_keys[0]
        data[key] = dummy_cuba_value(key) + dummy_cuba_value(key)
        with self.new_table('my_data_table') as table:
            uid = table.append(data)
            uid1 = uuid.uuid4()
            table[uid1] = data1
        with self.open_table('my_data_table') as table:
            self.assertEqual(len(table), 2)
            self.assertDataContainersEqual(table[uid], data)
            self.assertDataContainersEqual(table[uid1], data1)

    def test_update_data(self):
        saved_keys = self.saved_keys
        data = create_data_container(restrict=saved_keys)
        with self.new_table('my_data_table') as table:
            uid = table.append(data)
        with self.open_table('my_data_table', mode='a') as table:
            self.assertEqual(len(table), 1)
            key = saved_keys[0]
            data[key] = dummy_cuba_value(key) + dummy_cuba_value(key)
            table[uid] = data
            loaded_data = table[uid]
            self.assertDataContainersEqual(loaded_data, data)

    def test_update_data_with_missing_keywords(self):
        data = create_data_container(restrict=self.saved_keys[:-1])
        with self.new_table('my_data_table') as table:
            uid = table.append(data)
        with self.open_table('my_data_table', mode='a') as table:
            self.assertEqual(len(table), 1)
            for keys in data.keys()[:-1]:
                del data[keys]
            table[uid] = data
            loaded_data = table[uid]
            self.assertDataContainersEqual(loaded_data, data)

    def test_delete_data(self):
        saved_keys = self.saved_keys
        data = create_data_container(restrict=saved_keys)
        with self.new_table('my_data_table') as table:
            uid0 = table.append(data)
            new_data = DataContainer(data)
            key = saved_keys[0]
            data[key] = dummy_cuba_value(key) + dummy_cuba_value(key)
            uid1 = table.append(new_data)
        with self.open_table('my_data_table', mode='a') as table:
            del table[uid0]
            loaded_data = table[uid1]
            self.assertEqual(len(table), 1)
            self.assertDataContainersEqual(loaded_data, new_data)

    def test_delete_data_to_empty_table(self):
        data = create_data_container()
        with self.new_table('my_data_table') as table:
            uid = table.append(data)
        with closing(tables.open_file(self.filename, mode='a')) as handle:
            root = handle.root
            table = DataContainerTable(
                root, 'my_data_table', record=self.record)
            del table[uid]
            self.assertEqual(len(table), 0)
            # The table is recreated we need to make sure that the right
            # record is used.
            data_column = root.my_data_table.colinstances['Data']
            expected_column_names = [
                key.name.lower() for key in self.saved_keys]
            self.assertItemsEqual(
                data_column._v_colnames, expected_column_names)

    def test_iteration(self):
        # create sample data
        data = []
        saved_keys = self.saved_keys
        for key in saved_keys:
            data_container = create_data_container(restrict=saved_keys)
            del data_container[key]
            data.append(data_container)

        # add to data container table
        with self.new_table('my_data_table') as table:
            for data_container in data:
                table.append(data_container)
            self.assertEqual(len(table), len(saved_keys))

        # Iterate over all the rows
        with self.open_table('my_data_table') as table:
            for index, loaded_data in enumerate(table):
                self.assertDataContainersEqual(loaded_data, data[index])
            self.assertEqual(index,  len(saved_keys) - 1)

    def test_itersequence(self):
        # create sample data
        data = []
        saved_keys = self.saved_keys
        for key in saved_keys[:-1]:
            data_container = create_data_container(restrict=saved_keys)
            del data_container[key]
            data.append(data_container)

        # add to data container table
        with self.open_table('my_data_table', mode='a') as table:
            uids = {
                table.append(data_container): data_container
                for data_container in data}

            self.assertEqual(len(table), len(saved_keys) - 1)

        # Iterate over a sequence of rows
        with self.open_table('my_data_table') as table:
            sequence = random.sample(uids, 4)
            loaded_data = [
                container for container in table.itersequence(sequence)]
            self.assertEqual(len(loaded_data), 4)
            for index, container in enumerate(loaded_data):
                self.assertDataContainersEqual(
                    container, uids[sequence[index]])

    def assertDataContainersEqual(self, data1, data2):
        self.assertIsInstance(data1, DataContainer)
        self.assertIsInstance(data2, DataContainer)
        self.assertEqual(len(data1), len(data2))
        for key in data1:
            self.assertIn(key, data2)
            assert_equal(data1[key], data2[key])
