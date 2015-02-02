import unittest


from simphony.core.cuba import CUBA
from simphony.io.data_container_description import Record
from simphony.io.tests.abc_data_container_table_check import (
    ABCDataContainerTableCheck)


class TestDataContainerTable(
        ABCDataContainerTableCheck, unittest.TestCase):

    @property
    def record(self):
        return Record




if __name__ == '__main__':
    unittest.main()
