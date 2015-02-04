import tempfile
import abc
import shutil
import os
from contextlib import closing, contextmanager
from collections import OrderedDict

import tables
from numpy.testing import assert_equal

from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer
from simphony.io.indexed_data_container_table import IndexedDataContainerTable
from simphony.io.tests.utils import create_data_container, dummy_cuba_value


class ABCIndexedDataContainerTableCheck(object):

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
        self.filename = os.path.join(self.temp_dir, '__test_file.cuds')
        self.maxDiff = None

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    @contextmanager
    def new_table(self, table_name):
        handle = None
        try:
            handle = tables.open_file(self.filename, mode='w')
            root = handle.root
            table = IndexedDataContainerTable(
                root, table_name, record=self.record)
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
            table = IndexedDataContainerTable(
                root, table_name, record=self.record)
            yield table
        finally:
            if handle is not None:
                handle.close()

    @property
    def data_list(self):
        data = create_data_container(restrict=self.saved_keys)
        full_data = create_data_container()
        empty_data = DataContainer()
        reduced_data = create_data_container(restrict=self.saved_keys[:-1])
        return [data, empty_data, full_data, reduced_data]

    def test_creating_a_data_container_table(self):
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = IndexedDataContainerTable(
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
        with self.new_table('my_data_table') as table:
            indices = {table.append(data): data for data in self.data_list}
        with self.open_table('my_data_table') as table:
            self.assertEqual(len(table), 4)
            for index, data in indices.iteritems():
                if len(data) <= len(self.saved_keys):
                    self.assertDataContainersEqual(table[index], data)
                else:
                    # special case for custom records since they do not
                    # store the full set of keys
                    self.assertDataContainersEqual(
                        table[index],
                        create_data_container(restrict=self.saved_keys))

    def test_get_data(self):
        saved_keys = self.saved_keys
        data = create_data_container(restrict=saved_keys)
        data1 = DataContainer(data)
        key = saved_keys[0]
        data[key] = dummy_cuba_value(key) + dummy_cuba_value(key)
        with self.new_table('my_data_table') as table:
            table.append(data)
            table.append(data1)
        with self.open_table('my_data_table') as table:
            self.assertEqual(len(table), 2)
            self.assertDataContainersEqual(table[0], data)
            self.assertDataContainersEqual(table[1], data1)

    def test_get_with_invalid_index(self):
        saved_keys = self.saved_keys
        data = create_data_container(restrict=saved_keys)
        with self.new_table('my_data_table') as table:
            table.append(data)
        with self.open_table('my_data_table') as table:
            with self.assertRaises(IndexError):
                table[7]

    def test_set_with_invalid_index(self):
        saved_keys = self.saved_keys
        data = create_data_container(restrict=saved_keys)
        with self.new_table('my_data_table') as table:
            table.append(data)
        with self.open_table('my_data_table') as table:
            with self.assertRaises(IndexError):
                table[7] = data

    def test_update_data(self):
        with self.new_table('my_data_table') as table:
            indices = OrderedDict()
            for data in self.data_list:
                indices[table.append(data)] = data
        with self.open_table('my_data_table', mode='a') as table:
            updated_data = [data for data in reversed(self.data_list)]
            for index in indices:
                for data in updated_data:
                    table[index] = data
                    if len(data) <= len(self.saved_keys):
                        self.assertDataContainersEqual(table[index], data)
                    else:
                        # special case for custom records since they do not
                        # store the full set of keys
                        self.assertDataContainersEqual(
                            table[index],
                            create_data_container(restrict=self.saved_keys))

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

    def assertDataContainersEqual(self, data1, data2):
        self.assertIsInstance(data1, DataContainer)
        self.assertIsInstance(data2, DataContainer)
        self.assertEqual(len(data1), len(data2))
        for key in data1:
            self.assertIn(key, data2)
            assert_equal(data1[key], data2[key])
