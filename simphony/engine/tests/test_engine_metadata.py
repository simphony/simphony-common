"""Tests regarding loading engine's metadata."""
import unittest
from mock import patch

from simphony.api import CUDS
from simphony.cuds.abc_modeling_engine import ABCModelingEngine
from simphony.engine import ABCEngineExtension,\
    EngineInterface, get_engine_manager, get_supported_engine_names
from simphony.engine import get_supported_engines
from simphony.engine.extension import EngineManager, EngineManagerError
from simphony.engine.extension import EngineFeatureMetadata, EngineMetadata
from simphony.engine.decorators import register


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


@register
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


@patch('simphony.engine._ENGINE_MANAGER', new=EngineManager())
class TestEnginePublicAPI(unittest.TestCase):
    """Test everything engine metadata."""
    def test_get_supported_engines(self):
        supported = get_supported_engines()
        # TODO: inspect the returned metadata
        assert(isinstance(supported, list))

    def test_register_decorator(self):
        cls = get_example_engine_extension()
        self.assertNotIn('EXAMPLE2',
                         get_supported_engine_names())
        register(cls)
        self.assertIn('EXAMPLE2',
                      get_supported_engine_names())
        self.assertIn(cls.__name__,
                      get_engine_manager()._registry)

    def test_loaded_engines(self):
        self.assertNotIn('EXAMPLE1',
                         get_supported_engine_names())


class TestEngineManager(unittest.TestCase):
    """Test everything engine metadata."""
    def setUp(self):
        self.manager = EngineManager()
        # Load engines defined in this test moduel.
        self.manager.register_extension(_Example1)

    def test_get_supported_engines(self):
        supported = self.manager.get_supported_engine_names()
        self.assertIn('EXAMPLE1', supported)
        self.assertNotIn('EXAMPLE2', supported)

    def test_engine_count(self):
        supported = self.manager.get_supported_engine_names()
        self.assertEqual(len(supported), 1)

    def test_register_extension(self):
        cls = get_example_engine_extension()
        self.manager.register_extension(cls)
        self.assertIn(cls.__name__,
                      self.manager._registry)
        self.assertIn('EXAMPLE2',
                      self.manager.get_supported_engine_names())

    def test_duplicate_engine(self):
        cls = get_example_engine_extension()
        self.manager.register_extension(cls)
        cls.__name__ = 'some other name'
        self.assertRaisesRegexp(EngineManagerError,
                                'There is already an extension registered',
                                self.manager.register_extension,
                                cls)

    def test_duplicate_ignored(self):
        before = list(self.manager._registry)
        self.manager.register_extension(_Example1)
        self.assertEqual(before, self.manager._registry)

    def test_bad_extension(self):
        class SomethingElse(object):
            pass

        class BadExtension(ABCEngineExtension):
            def __new__(cls):
                return SomethingElse()

            def get_supported_engines(self):
                return []

            def create_wrapper(self, cuds, engine_name, engine_interface):
                return None

        self.assertRaisesRegexp(ValueError,
                                'Expected ABCEngineExtension, got',
                                self.manager.register_extension,
                                BadExtension)

    def test_add_extension(self):
        cls = get_example_engine_extension()
        self.manager.register_extension(cls)
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

        # Explicitly add example2 engine
        cls = get_example_engine_extension()
        self.manager.register_extension(cls)
        example2 = \
            self.manager.create_wrapper(cuds,
                                        'EXAMPLE2',
                                        EngineInterface.Internal)
        self.assertIsInstance(example2, DummyEngine2)
        self.assertEqual(cuds, example2.get_cuds())

    def test_non_module_load(self):
        class MyClass(object):
            pass

        self.assertRaisesRegexp(EngineManagerError,
                                'Not valid engine metadata',
                                self.manager.register_extension,
                                MyClass)


class TestEngineFeature(unittest.TestCase):
    """Test everything engine metadata."""
    def test_init(self):
        self.assertRaises(EngineManagerError,
                          EngineFeatureMetadata, None, None)
        self.assertRaises(EngineManagerError,
                          EngineFeatureMetadata, None, [])


class TestEngineMetadata(unittest.TestCase):
    """Test everything engine metadata."""
    def test_init(self):
        m = EngineMetadata('myengine', None, EngineInterface.Internal)
        self.assertEqual(m.name, 'myengine')
        self.assertEqual(m.features, None)
        self.assertEqual(m.interfaces, EngineInterface.Internal)
