import unittest
import numpy

from simphony.api import CUBA
from simphony.core.keywords import KEYWORDS
from simphony.cuds.meta import api
from simphony.cuds.meta.validation import\
    (decode_shape,
     check_shape,
     validate_cuba_keyword)


class TestValidation(unittest.TestCase):

    def test_decode_shape(self):
        self.assertEqual(decode_shape('(:)'), ((-numpy.inf, numpy.inf),))
        self.assertEqual(decode_shape('()'), ())
        self.assertEqual(decode_shape('(1,)'), ((1, 1),))
        self.assertEqual(decode_shape('(:, 10:, 1:2, :5)'),
                         ((-numpy.inf, numpy.inf),
                          (10, numpy.inf),
                          (1, 2),
                          (-numpy.inf, 5)))
        self.assertEqual(decode_shape('(-anything:anything)'),
                         ((-numpy.inf, numpy.inf),))

    def test_check_shape_simple(self):
        # These values are valid for the given `shape`
        # '()' means it can be of any shape
        self.assertIsNone(check_shape((1, 2), '()'))
        self.assertIsNone(check_shape((1, 2), '(2)'))
        self.assertIsNone(check_shape(((1, 2, 3), (4, 5, 6)),  # shape: (2, 3)
                                      '(:2, :3)'))

    def test_check_shape_special(self):
        ''' Test for value=1 and value=[1] to be both valid for shape=(1) '''
        # FIXME: In the cuba.yml, shape = [1] is used to say there is only
        # one value, while in the simphony_metadata.yml shape = (1) is used to
        # mean it is a sequence of only one value.  Accomodating the two means
        # we have to treat value = 1.0 and value = (1.0,) to be of compatible
        # shape
        self.assertIsNone(check_shape(0.1, '(1)'))
        self.assertIsNone(check_shape(0.1, '(1,)'))
        self.assertIsNone(check_shape((0.1,), '(1)'))
        self.assertIsNone(check_shape(0.1, '()'))

    def test_error_check_shape(self):
        ''' Test for ValueError for invalid shapes '''
        # These are values that are invalid for the given `shape`
        invalid_examples = (
            # value, required_shape
            ((1, 2, 3), '(2)'),
            (0.2, '(2)'),
            ((1, 2, 3, 4), '(:3)'),
            ((1, 2), '(3:)'),
            (((1, 2, 3), (4, 5, 6)), '(:1, :2)'))

        for value, required_shape in invalid_examples:
            try:
                check_shape(value, required_shape)
            except ValueError:
                pass
            else:
                msg = 'ValueError is not raised for value: {}, shape: {}'
                self.fail(msg.format(value, required_shape))

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
