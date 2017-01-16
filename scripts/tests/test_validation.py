import unittest

from simphony.core.keywords import KEYWORDS
from simphony.cuds.meta import api
from simphony.cuds.meta.validation import \
    (check_valid_shape,
     validate_cuba_keyword)


class TestValidation(unittest.TestCase):

    def test_check_shape_simple(self):
        # These values are valid for the given `shape`
        self.assertIsNone(
            check_valid_shape(
                ((1, 2, 3), (4, 5, 6)),  # shape: (2, 3)
                (2, 3),
                "CUBA.MINOR"
            ))

        self.assertIsNone(
            check_valid_shape([1, 2, 3],
                              [1],
                              'CUBA.ACCELERATION')
        )

    def test_validate_cuba_keyword(self):
        ''' Test for valid cases for CUBA keyword values '''
        # Check valid cases
        self.assertIsNone(validate_cuba_keyword(1.0, 'time_step'))
        self.assertIsNone(validate_cuba_keyword(api.Material(), 'material'))
        self.assertIsNone(validate_cuba_keyword('Hi', 'name'))

    def test_error_validate_cuba_keyword(self):
        ''' Test for TypeError for invalid CUBA keyword value '''
        invalid_examples = (
            (1, 'NAME'),             # type: str
            (range(2), 'velocity'),  # shape: (3)
            (1.0, 'material_type'),  # type: int
            (1, 'CUBA.POSITION'),    # type: double
            (api.CUDSItem(), 'CUBA.MATERIAL'),  # not instance of Material
        )

        for value, cuba_name in invalid_examples:
            try:
                validate_cuba_keyword(value, cuba_name)
            except (TypeError, ValueError):
                pass
            else:
                msg = ('Error is not raised for {cuba}: {value}'
                       '{cuba} should be a {type} with shape {shape}')
                key = cuba_name.upper()
                if key.startswith('CUBA.'):
                    key = key[5:]
                self.fail(msg.format(cuba=cuba_name, value=value,
                                     type=KEYWORDS[key].dtype,
                                     shape=KEYWORDS[key].dtype))
