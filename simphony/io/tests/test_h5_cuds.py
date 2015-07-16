import unittest
import os
import uuid
from contextlib import closing
import shutil
import tempfile
import tables

from simphony.cuds.particles import Particle, Particles
from simphony.cuds.mesh import Point, Mesh

from simphony.core.cuba import CUBA
from simphony.io.h5_cuds import H5CUDS
from simphony.io.h5_mesh import H5Mesh
from simphony.io.h5_particles import H5Particles
from simphony.io.h5_lattice import H5Lattice

from simphony.testing.abc_check_engine import (
    ParticlesCudsCheck, MeshCudsCheck,
    LatticeCudsCheck)


class TestH5CUDS(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.maxDiff = None
        self.particles = []
        self.points = []
        for i in xrange(10):
            self.particles.append(
                Particle((1.1*i, 2.2*i, 3.3*i), uid=uuid.uuid4()))
            self.points.append(Point((1.1*i, 2.2*i, 3.3*i), uid=uuid.uuid4()))

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

    def test_add_get_particle_container_data(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        original_pc = Particles(name="test")
        # Change data
        data = original_pc.data
        data[CUBA.NAME] = 'somename'
        original_pc.data = data

        # Store particle container along with its data
        with closing(H5CUDS.open(filename)) as handle:
            pc = handle.add_dataset(original_pc)

        # Reopen the file and check the data if it is still there
        with closing(H5CUDS.open(filename, 'r')) as handle:
            pc = handle.get_dataset('test')
            self.assertIn(CUBA.NAME, pc.data)
            self.assertEqual(pc.data[CUBA.NAME], 'somename')

    def test_add_get_particle_container(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        filename_copy = os.path.join(self.temp_dir, 'test-copy.cuds')
        with closing(H5CUDS.open(filename, 'w')) as handle:
            # add particle container and add points to it
            handle.add_dataset(Particles(name="test"))
            pc_test = handle.get_dataset("test")
            uids = pc_test.add_particles(self.particles)
            for particle in self.particles:
                uid = particle.uid
                self.assertIn(uid, uids)
                self.assertEqual(
                    particle.coordinates,
                    pc_test.get_particle(uid).coordinates)
            self.assertEqual(
                len(self.particles), sum(1 for _ in pc_test.iter_particles()))

            # add the particle container from the first file
            # into the second file
            with closing(H5CUDS.open(filename_copy, 'w')) as handle_copy:
                handle_copy.add_dataset(pc_test)
                pc_copy = handle_copy.get_dataset(pc_test.name)

                for particle in pc_test.iter_particles():
                    particle_copy = pc_copy.get_particle(particle.uid)
                    self.assertEqual(particle_copy.uid, particle.uid)
                    self.assertEqual(
                        particle_copy.coordinates, particle.coordinates)

    def test_add_get_mesh(self):
        # add mesh and add points to it
        filename = os.path.join(self.temp_dir, 'test.cuds')
        filename_copy = os.path.join(self.temp_dir, 'test-copy.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            handle.add_dataset(Mesh(name="test"))
            m_test = handle.get_dataset("test")
            for p in self.points:
                uid = m_test.add_point(p)
                self.assertEqual(p.uid, uid)
                self.assertEqual(
                    p.coordinates, m_test.get_point(uid).coordinates)

            num_points = sum(1 for _ in m_test.iter_points())
            self.assertEqual(num_points, len(self.points))

            # add the mesh from the first file into the second file
            with closing(H5CUDS.open(filename_copy)) as handle_copy:
                handle_copy.add_dataset(m_test)
                m_copy = handle_copy.get_dataset(m_test.name)

                for p in m_test.iter_points():
                    p1 = m_copy.get_point(p.uid)
                    self.assertEqual(p1.uid, p.uid)
                    self.assertEqual(p1.coordinates, p.coordinates)

        with self.assertRaises(Exception):
            m_test.delete(self.points[0].uid)
        with self.assertRaises(Exception):
            handle.get_dataset('test')

        # reopen file (in read only mode)
        with closing(H5CUDS.open(filename, 'r')) as handle:
            m_test = handle.get_dataset('test')
            for p in self.points:
                p1 = m_test.get_point(p.uid)
                self.assertEqual(p1.uid, p.uid)
                self.assertEqual(p1.coordinates, p.coordinates)


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


class TestParticlesCudsOperations(ParticlesCudsCheck, unittest.TestCase):

    def setUp(self):
        ParticlesCudsCheck.setUp(self)
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

    def tearDown(self):
        for engine in self.engines:
            engine.close()


class TestMeshCudsOperations(MeshCudsCheck, unittest.TestCase):

    def setUp(self):
        MeshCudsCheck.setUp(self)
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

    def tearDown(self):
        for engine in self.engines:
            engine.close()


class TestLatticeCudsOperations(LatticeCudsCheck, unittest.TestCase):

    def setUp(self):
        LatticeCudsCheck.setUp(self)
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

    def tearDown(self):
        for engine in self.engines:
            engine.close()


if __name__ == '__main__':
    unittest.main()
