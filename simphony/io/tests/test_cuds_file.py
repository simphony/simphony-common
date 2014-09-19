import unittest
import os

import tables

from simphony.cuds.particle import Particle
from simphony.io.cuds_file import CudsFile
from simphony.io.file_particle_container import FileParticleContainer


class TestCudsFile(unittest.TestCase):

    def setUp(self):
        # create some particles
        self.particles = []
        for i in xrange(10):
            self.particles.append(Particle((1.1*i, 2.2*i, 3.3*i), id=i))

        self.file_a = CudsFile.open('test_A.cuds')
        self.file_b = CudsFile.open('test_B.cuds')

    def tearDown(self):
        self.file_a.close()
        self.file_b.close()
        os.remove('test_A.cuds')
        os.remove('test_B.cuds')

    def test_init_with_append_mode(self):
        file = CudsFile.open('test.cuds', mode='a')
        self.assertTrue(file.valid())
        file.close()
        os.remove('test.cuds')

    def test_init_with_write_mode(self):
        file = CudsFile.open('test.cuds', mode='w')
        self.assertTrue(file.valid())
        file.close()
        os.remove('test.cuds')

    def test_init_with_unsupported_mode(self):
        with self.assertRaises(Exception):
            file = CudsFile.open('test.cuds', mode='x')
            file.valid()

    def test_init_with_read_only_mode(self):
        file = CudsFile.open('test.cuds', mode='w')
        file.close()

        with self.assertRaises(Exception):
            file = CudsFile.open('test.cuds', mode='r')
        os.remove('test.cuds')

    def test_init_with_read_only_file(self):
        with tables.open_file('test.cuds', mode="w"):
            pass

        with tables.open_file('test.cuds', mode="r") as pfile:
            with self.assertRaises(Exception):
                CudsFile(pfile)
        os.remove('test.cuds')

    def test_init_with_non_file(self):
        with self.assertRaises(Exception):
            CudsFile(None)

    def test_valid(self):
        self.assertTrue(self.file_a.valid())
        self.file_a.close()
        self.assertFalse(self.file_a.valid())
        self.file_a = CudsFile.open('test_A.cuds')
        self.assertTrue(self.file_a.valid())

    def test_get_missing_particle_container(self):
        with self.assertRaises(ValueError):
            self.file_a.get_particle_container('foo')

    def test_add_particle_container_empty(self):
        pc = self.file_a.add_particle_container('test')
        self.assertEqual(0, len(list(b for b in pc.iter_particles())))
        self.assertEqual(0, len(list(p for p in pc.iter_bonds())))

    def test_add_particle_container_with_same_name(self):
        self.file_a.add_particle_container('test')
        with self.assertRaises(ValueError):
            self.file_a.add_particle_container('test')

    def test_add_get_particle_container(self):
        # add particle container and add points to it
        pc_test_a = self.file_a.add_particle_container('test')
        for p in self.particles:
            id = pc_test_a.add_particle(p)
            self.assertEqual(p.id, id)
            self.assertEqual(
                p.coordinates, pc_test_a.get_particle(id).coordinates)

        num_particles = len(list(p for p in pc_test_a.iter_particles()))
        self.assertEqual(num_particles, len(self.particles))

        # add the particle container from the first file
        # into the second file
        pc_test_b = self.file_b.add_particle_container("other_test", pc_test_a)

        for p in pc_test_a.iter_particles():
            p1 = pc_test_b.get_particle(p.id)
            self.assertEqual(p1.id, p.id)
            self.assertEqual(p1.coordinates, p.coordinates)

        # close file and test if we can access it
        self.file_a.close()
        with self.assertRaises(Exception):
            pc_test_a.delete(self.particles[0].id)
        with self.assertRaises(Exception):
            pc_closed_file = self.file_a.get_particle_container('test')
            pc_closed_file.delete(self.particles[0].id)

        # reopen file (in append mode)
        self.file_a = CudsFile.open('test_A.cuds')
        pc_test_a = self.file_a.get_particle_container('test')
        for p in self.particles:
            p1 = pc_test_a.get_particle(p.id)
            self.assertEqual(p1.id, p.id)
            self.assertEqual(p1.coordinates, p.coordinates)

    def test_iter_particle_container(self):
        pc_names = []
        # add a few empty particle containers
        for i in xrange(5):
            name = "test_" + str(i)
            pc_names.append(name)
            self.file_a.add_particle_container(name)

        # test iterating over all
        names = list(
            name for pc, name in self.file_a.iter_particle_containers())
        self.assertEquals(len(names), len(pc_names))
        for name in names:
            self.assertTrue(name in pc_names)

        # test iterating over a specific subset
        subset = pc_names[:3]
        names = list(
            name for pc, name in self.file_a.iter_particle_containers(subset))
        self.assertEquals(names, subset)

        for pc, name in self.file_a.iter_particle_containers(pc_names):
            self.assertTrue(isinstance(pc, FileParticleContainer))

    def test_delete_particle_container(self):
        pc_names = []

        # add a few empty particle containers
        for i in xrange(5):
            name = "test_" + str(i)
            pc_names.append(name)
            self.file_a.add_particle_container(name)

        # delete each of the particle containers
        for pc, name in self.file_a.iter_particle_containers():
            self.file_a.delete_particle_container(name)

            # test that we can't get deleted container
            with self.assertRaises(ValueError):
                self.file_a.get_particle_container(name)

            # test that we can't use the deleted container
            with self.assertRaises(Exception):
                pc.add_particle(self.particles[0])

    def test_delete_non_existing_particle_container(self):
            with self.assertRaises(ValueError):
                self.file_a.delete_particle_container("foo")

if __name__ == '__main__':
    unittest.main()
