import tempfile
import unittest
import shutil
import os
import random
from contextlib import closing


import tables
import numpy
from numpy.testing import assert_equal

from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer
from simphony.io.data_container_description import Record
from simphony.io.data_container_table import DataContainerTable


def create_data_container():
    """ Create a data container while respecting the expected data types.

    """
    members = CUBA.__members__
    data = {}
    Data = Record.columns['Data']

    for member, cuba in members.items():
        column_type = Data._v_colobjects[member.lower()]
        if numpy.issubdtype(column_type, str):
            data[cuba] = member
        elif numpy.issubdtype(column_type, numpy.float):
            data[cuba] = float(cuba + 3)
        elif numpy.issubdtype(column_type, numpy.integer):
            data[cuba] = int(cuba + 3)
        else:
            shape = column_type.shape
            if column_type.kind == 'float':
                data[cuba] = numpy.ones(
                    shape=shape, dtype=numpy.float64) * cuba + 3
            elif column_type.kind == 'int':
                data[cuba] = numpy.ones(
                    shape=shape, dtype=numpy.int32) * cuba + 3
            else:
                raise RuntimeError(
                    'cannot create value for {}'.format(column_type))

    return DataContainer(data)


class TestDataContainerTable(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, '_test_file.cuds')
        self.maxDiff = None

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_creating_a_data_container_table(self):
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            self.assertIn('my_data_table', root)
            self.assertTrue(table.valid)

    def test_append_data(self):
        data = DataContainer({key: key + 3 for key in CUBA})
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            self.assertEqual(len(table), 0)
            table.append(data)
        with closing(tables.open_file(self.filename, mode='r')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            self.assertEqual(len(table), 1)

    def test_append_data_with_missing_keywords(self):
        data = DataContainer({CUBA(i): CUBA(i) + 3 for i in range(20, 67)})
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            self.assertEqual(len(table), 0)
            table.append(data)
            self.assertEqual(len(table), 1)
            table.append(data)
            self.assertEqual(len(table), 2)
        with closing(tables.open_file(self.filename, mode='r')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            self.assertEqual(len(table), 2)

    def test_get_data(self):
        data = create_data_container()
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            uid = table.append(data)
        with closing(tables.open_file(self.filename, mode='r')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            loaded_data = table[uid]
            self.assertEqual(len(table), 1)
            self.assertDataContainersEqual(loaded_data, data)

    def test_get_data_with_missing_keywords(self):
        data = create_data_container()
        for i in range(20, 56):
            del data[CUBA(i)]
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            uid = table.append(data)
        with closing(tables.open_file(self.filename, mode='r')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            loaded_data = table[uid]
            self.assertDataContainersEqual(loaded_data, data)

    def test_update_data(self):
        data = create_data_container()
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            uid = table.append(data)
        with closing(tables.open_file(self.filename, mode='a')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            self.assertEqual(len(table), 1)
            data[CUBA.VELOCITY] = 45
            table[uid] = data
            loaded_data = table[uid]
            self.assertDataContainersEqual(loaded_data, data)

    def test_update_data_with_missing_keywords(self):
        data = create_data_container()
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            uid = table.append(data)
        with closing(tables.open_file(self.filename, mode='a')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            self.assertEqual(len(table), 1)
            for i in range(20, 56):
                del data[CUBA(i)]
            table[uid] = data
            loaded_data = table[uid]
            self.assertDataContainersEqual(loaded_data, data)

    def test_delete_data(self):
        data = create_data_container()
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            uid0 = table.append(data)
            new_data = DataContainer(data)
            new_data[CUBA.VELOCITY] = 45
            uid1 = table.append(new_data)
            del table[uid0]
            loaded_data = table[uid1]
            self.assertEqual(len(table), 1)
            self.assertDataContainersEqual(loaded_data, new_data)

    def test_delete_data_to_empty_table(self):
        data = create_data_container()
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            uid = table.append(data)
            del table[uid]
            self.assertEqual(len(table), 0)

    def test_iteration(self):
        # create sample data
        data = []
        for index in range(10):
            data_container = create_data_container()
            del data_container[CUBA(index + 3)]
            data.append(data_container)

        # add to data container table
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            for data_container in data:
                table.append(data_container)
            self.assertEqual(len(table), 10)

        # Iterate over all the rows
        with closing(tables.open_file(self.filename, mode='r')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            for index, loaded_data in enumerate(table):
                self.assertDataContainersEqual(loaded_data, data[index])
            self.assertEqual(index, 9)

    def test_itersequence(self):
        # create sample data
        data = []
        for index in range(10):
            data_container = create_data_container()
            del data_container[CUBA(index + 3)]
            data.append(data_container)

        # add to data container table
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            uids = {
                table.append(data_container): data_container
                for data_container in data}

            self.assertEqual(len(table), 10)

        # Iterate over a sequence of rows
        with closing(tables.open_file(self.filename, mode='r')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
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


if __name__ == '__main__':
    unittest.main()
