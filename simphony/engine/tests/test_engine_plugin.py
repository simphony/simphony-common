import unittest

try:
    import simphony_example  # noqa
except ImportError:
    EXAMPLE_NOT_INSTALLED = True
else:
    EXAMPLE_NOT_INSTALLED = False


@unittest.skipIf(EXAMPLE_NOT_INSTALLED, 'Example plugin not installed')
class TestEnginePlugin(unittest.TestCase):

    def test_load_plugin(self):
        try:
            from simphony.engine import example_engine
        except ImportError:
            self.fail('Could not import example engine')

        self.assertTrue(hasattr(example_engine, 'A'))
