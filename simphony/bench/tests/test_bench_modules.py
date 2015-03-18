import unittest
import importlib

BENCH_MODULES = [
    'cuds_file_bench',
    'data_container_bench',
    'data_container_table_bench',
    'indexed_data_container_table_bench',
    'util']


class TestBenchModules(unittest.TestCase):

    def test_imporiting(self):
        for module in BENCH_MODULES:
            name = '.'.join(('simphony', 'bench', module))
            importlib.import_module(name)


if __name__ == '__main__':
    unittest.main()
