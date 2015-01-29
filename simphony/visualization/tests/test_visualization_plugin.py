import unittest

try:
    import simphony_example  # noqa
except ImportError:
    EXAMPLE_NOT_INSTALLED = True
else:
    EXAMPLE_NOT_INSTALLED = False


@unittest.skipIf(EXAMPLE_NOT_INSTALLED, 'Example plugin not installed')
class TestVisualizationPlugin(unittest.TestCase):

    def test_load_plugin(self):
        try:
            from simphony.visualization import example
        except ImportError:
            self.fail('Could not import example visualization')

        self.assertTrue(hasattr(example, 'A'))
