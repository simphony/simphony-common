import unittest
import os
from contextlib import closing
import shutil
import tempfile

from simphony.io.h5_cuds import H5CUDS

from simphony.testing.abc_check_engine import (
    ParticlesCudsCheck, MeshCudsCheck,
    LatticeCudsCheck)


class TestH5CUDS(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.maxDiff = None

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_open_with_append_mode(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename, 'a')) as handle:
            self.assertTrue(handle.valid())

    def test_open_with_write_mode(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename, 'w')) as handle:
            self.assertTrue(handle.valid())

    def test_open_with_read_only_mode(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename, 'w')) as handle:
            self.assertTrue(handle.valid())
        with closing(H5CUDS.open(filename, 'r')) as handle:
            self.assertTrue(handle.valid())

    def test_init_with_non_file(self):
        with self.assertRaises(Exception):
            H5CUDS(None)

    def test_valid(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename, 'w')) as handle:
            self.assertTrue(handle.valid())
        self.assertFalse(handle.valid())
        with closing(H5CUDS.open(filename, 'a')) as handle:
            self.assertTrue(handle.valid())
        self.assertFalse(handle.valid())


class TestParticlesCudsOperations(ParticlesCudsCheck, unittest.TestCase):
    pass


class TestMeshCudsOperations(MeshCudsCheck, unittest.TestCase):
    pass


class TestLatticeCudsOperations(LatticeCudsCheck, unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
