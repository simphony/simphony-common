import tempfile
import unittest
import shutil
import os
from contextlib import closing

import tables

from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer
from simphony.io.data_container_table import DataContainerTable


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
            DataContainerTable(root, 'my_data_table')
            self.assertIn('my_data_table', root)

    def test_append_data(self):
        data = DataContainer({key: key + 3 for key in CUBA})
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            self.assertEqual(len(table), 0)
            table.append(data)
            self.assertEqual(len(table), 1)



if __name__ == '__main__':
    unittest.main()
