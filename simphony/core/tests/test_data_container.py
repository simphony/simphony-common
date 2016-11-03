import unittest

from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer


class TestDataContainer(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_initialization_with_a_dictionary(self):
        data = {key: 3 for key in CUBA}
        container = DataContainer(data)
        self.assertEqual(container, data)
        for key in container:
            self.assertIsInstance(key, CUBA)

    def test_initialization_with_a_iterable(self):
        data = [(key, 3) for key in CUBA]
        container = DataContainer(data)
        for key, value in data:
            self.assertEqual(container[key], value)
            self.assertIsInstance(key, CUBA)

    def test_initialization_with_keywords(self):
        data = {key: index + 3 for index, key in enumerate(CUBA.__members__)}
        container = DataContainer(**data)
        self.assertEqual(
            container, {key: index + 3 for index, key in enumerate(CUBA)})
        for key in container:
            self.assertIsInstance(key, CUBA)

    def test_initialization_with_keywords_and_iterable(self):
        data = {
            key: 3 for index, key in enumerate(CUBA.__members__)
            if key != str(CUBA("POTENTIAL_ENERGY"))[5:]}
        container = DataContainer([(CUBA("POTENTIAL_ENERGY"), 23)], **data)
        expected = {key: 3 for index, key in enumerate(CUBA)}
        expected[CUBA("POTENTIAL_ENERGY")] = 23
        self.assertDictEqual(container, expected)
        for key in container:
            self.assertIsInstance(key, CUBA)

    def test_initialization_with_non_cuba_kwards(self):
        with self.assertRaises(ValueError):
            DataContainer(bar=5)

    def test_initialization_with_non_cuba_dict(self):
        with self.assertRaises(ValueError):
            DataContainer({'foo': 5})

    def test_initialization_with_non_cuba_iterable(self):
        with self.assertRaises(ValueError):
            DataContainer([('foo', 5)])

    def test_initialization_with_multiple_arguments(self):
        with self.assertRaises(TypeError):
            DataContainer([('foo', 5)], 45)

    def test_initialization_with_a_dictionary_of_strings(self):
        data = {str(key): 3 for key in CUBA}
        with self.assertRaises(ValueError):
            DataContainer(data)

    def test_initialization_with_generator(self):
        generator = ((key, 3) for key in CUBA)
        container = DataContainer(generator)
        self.assertEqual(len(container), len(CUBA))

    def test_initialization_with_non_cuba_generator(self):
        generator = (('foo'+str(i), i) for i in range(5))
        with self.assertRaises(ValueError):
            DataContainer(generator)

    def test_update_with_a_dictionary(self):
        container = DataContainer()
        data = {key: 3 for key in CUBA}
        container.update(data)
        self.assertEqual(container, data)
        for key in container:
            self.assertIsInstance(key, CUBA)

    def test_update_with_a_dictionary_of_strings(self):
        container = DataContainer()
        data = {str(key): 3 for key in CUBA}
        with self.assertRaises(ValueError):
            container.update(data)

    def test_update_with_a_iterable(self):
        container = DataContainer()
        data = [(key,  3) for key in CUBA]
        container.update(data)
        # Check that has all the values
        for key, value in data:
            self.assertEqual(container[key], value)
            self.assertIsInstance(key, CUBA)

    def test_update_with_keywords(self):
        container = DataContainer()
        data = {key: index + 3 for index, key in enumerate(CUBA.__members__)}
        container.update(**data)
        self.assertEqual(
            container, {key: index + 3 for index, key in enumerate(CUBA)})
        for key in container:
            self.assertIsInstance(key, CUBA)

    def test_update_with_keywords_and_iterable(self):
        container = DataContainer()
        data = {
            key: 3 for index, key in enumerate(CUBA.__members__)
            if key != str(CUBA("POTENTIAL_ENERGY"))[5:]}
        container.update([(CUBA("POTENTIAL_ENERGY"), 23)], **data)
        expected = {key: index + 3 for index, key in enumerate(CUBA)}
        expected[CUBA("POTENTIAL_ENERGY")] = 23
        for key in container:
            self.assertIsInstance(key, CUBA)

    def test_update_with_non_cuba_kwards(self):
        container = DataContainer()
        with self.assertRaises(ValueError):
            container.update(bar=5)

    def test_update_with_non_cuba_dict(self):
        container = DataContainer()
        with self.assertRaises(ValueError):
            container.update({'foo': 5})

    def test_update_with_non_cuba_iterable(self):
        container = DataContainer()
        with self.assertRaises(ValueError):
            container.update([('foo', 5)])

    def test_setitem_with_int_key(self):
        container = DataContainer()
        with self.assertRaises(ValueError):
            container[10] = 29

    def test_setitem_with_cuba_key(self):
        container = DataContainer()
        container[CUBA("POTENTIAL_ENERGY")] = 29
        self.assertIsInstance(container.keys()[0], CUBA)
        self.assertEqual(container[CUBA("POTENTIAL_ENERGY")], 29)

    def test_setitem_with_non_cuba_key(self):
        container = DataContainer()
        with self.assertRaises(ValueError):
            container[100] = 29


if __name__ == '__main__':
    unittest.main()
