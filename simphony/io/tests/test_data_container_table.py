import unittest
from contextlib import closing

import tables

from simphony.io.data_container_description import Record
from simphony.io.data_container_table import DataContainerTable
from simphony.io.tests.abc_data_container_table_check import (
    ABCDataContainerTableCheck)


class CustomData(tables.IsDescription):

        name = tables.StringCol(pos=0, itemsize=20)
        direction = tables.Float64Col(pos=1, shape=3)
        status = tables.Int32Col(pos=2)
        label = tables.Int32Col(pos=3)
        material_id = tables.Int32Col(pos=4)
        chemical_specie = tables.StringCol(pos=5, itemsize=20)
        rolling_friction = tables.Float64Col(pos=6)
        volume_fraction = tables.Float64Col(pos=7)


class CustomRecord(tables.IsDescription):

    index = tables.StringCol(itemsize=16, pos=0)
    data = CustomData()
    mask = tables.BoolCol(pos=1, shape=(8,))


class TestDataContainerTable(
        ABCDataContainerTableCheck, unittest.TestCase):

    @property
    def record(self):
        return Record

    def test_creating_a_data_container_table_using_default_record(self):
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            table = DataContainerTable(root, 'my_data_table')
            self.assertEqual(len(table), 0)
            self.assertIn('my_data_table', root)
            self.assertTrue(table.valid)
            data_column = root.my_data_table.colinstances['data']
            expected_column_names = [
                key.name.lower() for key in self.saved_keys]
            self.assertItemsEqual(
                data_column._v_colnames, expected_column_names)


class TestDataContainerTableWithCustomRecord(
        ABCDataContainerTableCheck, unittest.TestCase):

    @property
    def record(self):
        return CustomRecord


if __name__ == '__main__':
    unittest.main()
