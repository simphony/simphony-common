import unittest

import tables

from simphony.io.data_container_description import Record
from simphony.io.tests.abc_data_container_table_check import (
    ABCDataContainerTableCheck)


class CustomRecord(tables.IsDescription):

    index = tables.StringCol(itemsize=16, pos=0)

    class Data(tables.IsDescription):

        name = tables.StringCol(pos=0, itemsize=20)
        direction = tables.Float64Col(pos=1, shape=3)
        status = tables.Int32Col(pos=2)
        label = tables.Int32Col(pos=3)
        material_id = tables.Int32Col(pos=4)
        chemical_specie = tables.StringCol(pos=5, itemsize=20)
        rolling_friction = tables.Float64Col(pos=6)
        volume_fraction = tables.Float64Col(pos=7)

    mask = tables.BoolCol(pos=1, shape=(8,))


class TestDataContainerTable(
        ABCDataContainerTableCheck, unittest.TestCase):

    @property
    def record(self):
        return Record


class TestDataContainerTableWithCustomRecord(
        ABCDataContainerTableCheck, unittest.TestCase):

    @property
    def record(self):
        return CustomRecord


if __name__ == '__main__':
    unittest.main()
