import unittest
import os
from contextlib import closing
import shutil
import tempfile
import tables

from simphony.core.cuds_item import CUDSItem
from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer
from simphony.io.h5_cuds import H5CUDS
from simphony.io.h5_mesh import H5Mesh
from simphony.io.h5_particles import H5Particles
from simphony.io.h5_lattice import H5Lattice
from simphony.cuds import Mesh, Particles
from simphony.cuds.lattice import make_cubic_lattice

from simphony.testing.abc_check_engine import (
    ParticlesEngineCheck, MeshEngineCheck,
    LatticeEngineCheck)


class TestH5CUDS(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

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

    def test_closed_file_not_usable(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            handle.add_dataset(Mesh(name="test_1"))
            handle.add_dataset(Particles(name="test_2"))
            lattice = make_cubic_lattice("test_3", 1.0, (2, 3, 4))
            handle.add_dataset(lattice)
            test_h1 = handle.get_dataset("test_1")
            test_h2 = handle.get_dataset("test_2")
            test_h3 = handle.get_dataset("test_3")
        with self.assertRaises(Exception):
            handle.get_dataset('test_h1')
        with self.assertRaises(Exception):
            test_h1.name = 'foo'
        with self.assertRaises(Exception):
            test_h2.name = 'foo'
        with self.assertRaises(Exception):
            test_h3.name = 'foo'


class TestH5CUDSVersions(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.existing_filename = os.path.join(self.temp_dir, 'test.cuds')
        handle = H5CUDS.open(self.existing_filename)
        handle.close()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_version(self):
        with closing(tables.open_file(
                     self.existing_filename, mode="r")) as h5file:
            self.assertTrue(isinstance(h5file.root._v_attrs.cuds_version, int))

    def test_incorrect_version(self):
        with closing(tables.open_file(
                     self.existing_filename, mode="a")) as h5file:
            h5file.root._v_attrs.cuds_version = -1

        with self.assertRaises(ValueError):
            H5CUDS.open(self.existing_filename)


class TestParticlesCudsOperations(ParticlesEngineCheck, unittest.TestCase):

    def setUp(self):
        ParticlesEngineCheck.setUp(self)
        self.temp_dir = tempfile.mkdtemp()
        self.engines = []

    def engine_factory(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        engine = H5CUDS.open(filename)
        self.engines.append(engine)
        return engine

    def check_instance_of_dataset(self, ds):
        """ Check if a dataset is instance of a class

        """
        self.assertTrue(isinstance(ds, H5Particles))

    def test_add_get_dataset_with_cuba_keys_argument(self):
        engine = self.engine_factory()
        items = self.create_dataset_items()
        reference = self.create_dataset(name='test')
        expected = self.create_dataset(name='test')

        # Add some CUBA data
        for particle in items:
            particle.data = DataContainer({CUBA.VELOCITY: [1, 0, 0]})
            expected.add_particles([particle])
            particle.data = DataContainer(
                {CUBA.VELOCITY: [1, 0, 0], CUBA.MASS: 1})
            reference.add_particles([particle])

        # Store reference dataset along with its data
        engine.add_dataset(reference, {CUDSItem.PARTICLE: [CUBA.VELOCITY]})

        # Closing and reopening the file
        engine.close()
        engine = self.engine_factory()

        ds = engine.get_dataset('test')
        self.compare_dataset(ds, expected)

    def tearDown(self):
        for engine in self.engines:
            engine.close()


class TestMeshCudsOperations(MeshEngineCheck, unittest.TestCase):

    def setUp(self):
        MeshEngineCheck.setUp(self)
        self.temp_dir = tempfile.mkdtemp()
        self.engines = []

    def engine_factory(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        engine = H5CUDS.open(filename)
        self.engines.append(engine)
        return engine

    def check_instance_of_dataset(self, ds):
        """ Check if a dataset is instance of a class

        """
        self.assertTrue(isinstance(ds, H5Mesh))

    def test_add_get_dataset_with_cuba_keys_argument(self):
        engine = self.engine_factory()
        items = self.create_dataset_items()
        reference = self.create_dataset(name='test')
        expected = self.create_dataset(name='test')

        # Add some CUBA data
        for point in items:
            point.data = DataContainer({CUBA.VELOCITY: [1, 0, 0]})
            expected.add_points([point])
            point.data = DataContainer(
                {CUBA.VELOCITY: [1, 0, 0], CUBA.MASS: 1})
            reference.add_points([point])

        # Store reference dataset along with its data
        engine.add_dataset(reference, {CUDSItem.POINT: [CUBA.VELOCITY]})

        # Closing and reopening the file
        engine.close()
        engine = self.engine_factory()

        ds = engine.get_dataset('test')
        self.compare_dataset(ds, expected)

    def tearDown(self):
        for engine in self.engines:
            engine.close()


class TestLatticeCudsOperations(LatticeEngineCheck, unittest.TestCase):

    def setUp(self):
        LatticeEngineCheck.setUp(self)
        self.temp_dir = tempfile.mkdtemp()
        self.engines = []

    def engine_factory(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        engine = H5CUDS.open(filename)
        self.engines.append(engine)
        return engine

    def check_instance_of_dataset(self, ds):
        """ Check if a dataset is instance of a class

        """
        self.assertTrue(isinstance(ds, H5Lattice))

    def test_add_get_dataset_with_cuba_keys_argument(self):
        engine = self.engine_factory()
        reference = self.create_dataset(name='test')
        expected = self.create_dataset(name='test')

        # Add some CUBA data
        for node in reference.iter_nodes():
            node.data = DataContainer({CUBA.MATERIAL_ID: 1})
            expected.update_nodes([node])
            node.data = DataContainer({CUBA.MATERIAL_ID: 1, CUBA.DENSITY: 2})
            reference.update_nodes([node])

        # Store reference dataset along with its data
        engine.add_dataset(reference, {CUDSItem.NODE: [CUBA.MATERIAL_ID]})

        # Closing and reopening the file
        engine.close()
        engine = self.engine_factory()

        ds = engine.get_dataset('test')
        self.compare_dataset(ds, expected)

    def tearDown(self):
        for engine in self.engines:
            engine.close()


if __name__ == '__main__':
    unittest.main()
