"""Tests regarding loading engine's metadata."""
import sys
import unittest

import simphony.engine as engine_api
from simphony.engine import ABCEngineExtension, EngineInterface
from simphony.engine.extension import EngineManager, EngineManagerException
from simphony.engine.extension import EngineFeatureMetadata, EngineMetadata


class _Example1(ABCEngineExtension):
    def get_supported_engines(self):
        example_engine = \
            self.create_engine_metadata('EXAMPLE1',
                                        None,
                                        [EngineInterface.Internal,
                                         EngineInterface.FileIO])

        return [example_engine]

    def create_wrapper(self, cuds, engine_name, engine_interface):
        if engine_name == 'EXAMPLE1':
            pass
        else:
            raise Exception('Only EXAMPLE1 engine is supported. '
                            'Unsupported eninge: %s', engine_name)


def get_example_engine_extension():
    class _Example2(ABCEngineExtension):
        def get_supported_engines(self):
            example_engine = \
                self.create_engine_metadata('EXAMPLE2',
                                            None,
                                            [EngineInterface.Internal,
                                             EngineInterface.FileIO])

            return [example_engine]

        def create_wrapper(self, cuds, engine_name, engine_interface):
            if engine_name == 'EXAMPLE2':
                pass
            else:
                raise Exception('Only EXAMPLE2 engine is supported. '
                                'Unsupported eninge: %s', engine_name)
    return _Example2


class TestEnginePublicAPI(unittest.TestCase):
    """Test everything engine metadata."""
    def setUp(self):
        self.manager = engine_api._ENGINE_MANAGER

    def tearDown(self):
        pass

    def test_get_supported_engines(self):
        supported = engine_api.get_supported_engines()
        assert(isinstance(supported, list))

    def test_create_wrapper(self):
        pass


class TestEngineManager(unittest.TestCase):
    """Test everything engine metadata."""
    def setUp(self):
        self.manager = EngineManager()
        self.manager.load_metadata(sys.modules[__name__])

    def tearDown(self):
        pass

    def test_get_supported_engines(self):
        supported = self.manager.get_supported_engine_names()
        self.assertIn('EXAMPLE1', supported)
        self.assertNotIn('LAMMPS', supported)

    def test_engine_count(self):
        supported = self.manager.get_supported_engine_names()
        self.assertEqual(len(supported), 1)

    def test_assert_duplicate_engine(self):
        self.assertRaises(Exception,
                          self.manager.load_metadata, sys.modules[__name__])

    def test_add_extension(self):
        cls = get_example_engine_extension()
        self.manager.add_extension(cls())
        supported = self.manager.get_supported_engine_names()
        self.assertIn('EXAMPLE2', supported)
        self.assertEqual(len(supported), 2)

    def test_create_wrapper(self):
        self.assertRaises(EngineManagerException,
                          self.manager.create_wrapper, None, 'EXAMPLE2')
        # Example is a dummpy engine. It does not have any wrapper.
        self.assertEqual(self.manager.create_wrapper(None, 'EXAMPLE1'), None)

    def test_non_module_load(self):
        class MyClass:
            pass
        self.assertRaises(EngineManagerException,
                          self.manager.load_metadata, MyClass)


class TestEngineFeature(unittest.TestCase):
    """Test everything engine metadata."""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        self.assertRaises(EngineManagerException,
                          EngineFeatureMetadata, None, None)
        self.assertRaises(EngineManagerException,
                          EngineFeatureMetadata, None, [])


class TestEngineMetadata(unittest.TestCase):
    """Test everything engine metadata."""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        m = EngineMetadata('myengine', None, EngineInterface.Internal)
        self.assertEqual(m.name, 'myengine')
        self.assertEqual(m.features, None)
        self.assertEqual(m.interfaces, EngineInterface.Internal)
