import unittest

from numpy.testing import assert_array_equal


from simphony.io.data_conversion import (convert_to_file_type,
                                         convert_from_file_type)
from simphony.core.cuba import CUBA
from simphony.testing.utils import dummy_cuba_value


class TestDataConversion(unittest.TestCase):

    def test_convert_all(self):
        for cuba in CUBA:
            # given
            original_value = dummy_cuba_value(cuba)

            # when
            file_value = convert_to_file_type(original_value, cuba)

            # then
            assert_array_equal(original_value,
                               convert_from_file_type(file_value, cuba))


if __name__ == '__main__':
    unittest.main()
