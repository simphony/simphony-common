"""Tests regarding loading engine's metadata."""
import sys
import unittest

import simphony.engine as engine_api
from simphony import CUDS
from simphony.cuds.abc_modeling_engine import ABCModelingEngine
from simphony.extension import ABCEngineExtension, EngineInterface
from simphony.extension.extension import EngineManager, EngineManagerException
from simphony.extension.extension import EngineFeatureMetadata, EngineMetadata


class DummyEngine(ABCModelingEngine):
    def __init__(self, *args, **kwargs):
        self._cuds = kwargs.get('cuds')
        self._load_cuds()

    def _load_cuds(self):
        pass

    def get_cuds(self):
        return self._cuds

    def run(self):
        pass

    def add_dataset(self, container):
        pass

    def remove_dataset(self, name):
        pass

    def get_dataset(self, name):
        pass

    def get_dataset_names(self):  # pragma: no cover
        pass

    def iter_datasets(self, names=None):  # pragma: no cover
        pass


class DummyEngine1(DummyEngine):
    pass


class DummyEngine2(DummyEngine):
    pass


class _Example1(ABCEngineExtension):
    """A dummy engine extension."""
    def get_supported_engines(self):
        example_engine = \
            self.create_engine_metadata('EXAMPLE1',
                                        None,
                                        [EngineInterface.Internal,
                                         EngineInterface.FileIO])

        return [example_engine]

    def create_wrapper(self, cuds, engine_name, engine_interface):
        if engine_name != 'EXAMPLE1':
            raise Exception('Only EXAMPLE1 engine is supported. '
                            'Unsupported eninge: %s', engine_name)
        return DummyEngine1(cuds=cuds)


def get_example_engine_extension():
    """A dummy engine extension."""
    class _Example2(ABCEngineExtension):
        def get_supported_engines(self):
            example_engine = \
                self.create_engine_metadata('EXAMPLE2',
                                            None,
                                            [EngineInterface.Internal,
                                             EngineInterface.FileIO])
            return [example_engine]

        def create_wrapper(self, cuds, engine_name, engine_interface):
            if engine_name != 'EXAMPLE2':
                raise Exception('Only EXAMPLE2 engine is supported. '
                                'Unsupported eninge: %s', engine_name)
            return DummyEngine2(cuds=cuds)
    return _Example2


class TestEnginePublicAPI(unittest.TestCase):
    """Test everything engine metadata."""
    def test_get_supported_engines(self):
        supported = engine_api.get_supported_engines()
        # TODO: inspect the returned metadata
        assert(isinstance(supported, list))


class TestEngineManager(unittest.TestCase):
    """Test everything engine metadata."""
    def setUp(self):
        self.manager = EngineManager()
        # Load engines defined in this test moduel.
        self.manager.load_metadata(sys.modules[__name__])

    def test_get_supported_engines(self):
        supported = self.manager.get_supported_engine_names()
        self.assertIn('EXAMPLE1', supported)
        self.assertNotIn('EXAMPLE2', supported)

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
        cuds = CUDS()
        example1 = \
            self.manager.create_wrapper(cuds,
                                        'EXAMPLE1',
                                        EngineInterface.Internal)
        self.assertIsInstance(example1, DummyEngine1)
        self.assertEqual(cuds, example1.get_cuds())

        # Explicitely add example2 engine
        cls = get_example_engine_extension()
        self.manager.add_extension(cls())
        example2 = \
            self.manager.create_wrapper(cuds,
                                        'EXAMPLE2',
                                        EngineInterface.Internal)
        self.assertIsInstance(example2, DummyEngine2)
        self.assertEqual(cuds, example2.get_cuds())

    def test_non_module_load(self):
        class MyClass:
            pass
        self.assertRaises(EngineManagerException,
                          self.manager.load_metadata, MyClass)


class TestEngineFeature(unittest.TestCase):
    """Test everything engine metadata."""
    def test_init(self):
        self.assertRaises(EngineManagerException,
                          EngineFeatureMetadata, None, None)
        self.assertRaises(EngineManagerException,
                          EngineFeatureMetadata, None, [])


class TestEngineMetadata(unittest.TestCase):
    """Test everything engine metadata."""
    def test_init(self):
        m = EngineMetadata('myengine', None, EngineInterface.Internal)
        self.assertEqual(m.name, 'myengine')
        self.assertEqual(m.features, None)
        self.assertEqual(m.interfaces, EngineInterface.Internal)
