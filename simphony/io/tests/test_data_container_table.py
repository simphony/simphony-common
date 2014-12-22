import tempfile
import unittest
import shutil
import os
from contextlib import closing

import tables
import numpy

from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer
from simphony.io.data_container_table import DataContainerTable
from simphony.io.data_container_description import Data


class TestDataContainerTable(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
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
            self.assertEqual(len(table), 1)

    def test_append_data_with_missing_keywords(self):
        data = DataContainer({CUBA(i): CUBA(i) + 3 for i in range(20, 67)})
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            self.assertEqual(len(table), 0)
            table.append(data)
            self.assertEqual(len(table), 1)

    def test_get_data(self):
        data = self.create_data_container()
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            table.append(data)
            loaded_data = table[0]
            self.assertItemsEqual(loaded_data.items(), loaded_data.items())

    def test_get_data_with_missing_keywords(self):
        data = self.create_data_container()
        for i in range(20, 56):
            del data[CUBA(i)]
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            table.append(data)
            loaded_data = table[0]
            self.assertItemsEqual(loaded_data.items(), loaded_data.items())

    def create_data_container(self):
        members = CUBA.__members__
        data = {}
        for member, cuba in members.items():
            column_type = Data.columns[member.lower()]
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


if __name__ == '__main__':
    unittest.main()
