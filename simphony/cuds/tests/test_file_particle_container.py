import unittest
import copy
from particle import Particle
import cuds_file
import os


class _EmptyParticleContainer():

    def iter_particles(self, ids=None):
        return
        yield


class TestFileParticleContainer(unittest.TestCase):

    def setUp(self):
        #create empty particle container and two particles (with unique ids)
        self.file = cuds_file.CudsFile()
        self.file.open('test_file.cuds')

        self.file.add_particle_container("test", _EmptyParticleContainer())

        self.pc = self.file.get_particle_container('test')
        self.particle_1 = Particle(0, (0.1, 0.4, 5.0))
        self.particle_2 = Particle(1, (0.2, 0.45, 50.0))

    def tearDown(self):
        self.file.close()
        os.remove('test_file.cuds')

    def test_add_get__particle(self):
        self.pc.add_particle(self.particle_1)
        particles = self.pc.get_particle(self.particle_1.id)
        self.assertTrue(particles is not self.particle_1)
        self.assertEqual(particles.id, self.particle_1.id)
        self.assertEqual(particles.coordinates, self.particle_1.coordinates)

    def test_add_particle_with_same_id(self):
        self.pc.add_particle(self.particle_1)
        with self.assertRaises(Exception):
            self.pc.add_particle(self.particle_1)

    def test_get_particle_throws(self):
        with self.assertRaises(Exception):
            self.pc.get_particle(0)

    def test_update_particle(self):
        with self.assertRaises(Exception):
            self.pc.update_particle(self.particle_1)

        self.pc.add_particle(self.particle_1)
        self.pc.add_particle(self.particle_2)
        p = copy.deepcopy(self.particle_1)
        p.coordinates = (42, 42, 42)
        self.pc.update_particle(p)
        updated_p = self.pc.get_particle(p.id)

        self.assertEqual(p, updated_p)
        self.assertNotEqual(p, self.particle_1)

    def test_iter_particles(self):
        particles1 = [self.particle_1, self.particle_2]
        for particle in particles1:
            self.pc.add_particle(particle)

        # test iterating particles without giving ids
        particles2 = list(p for p in self.pc.iter_particles())

        self.assertEquals(len(particles1), len(particles2))
        for particle in particles1:
            self.assertTrue(particle in particles2)

        # test iterating particles by giving ids
        particles1 = [self.particle_1, self.particle_2]
        ids1 = list(p.id for p in particles1)
        particles2 = list(p for p in self.pc.iter_particles(ids1))
        self.assertEqual(particles1, particles2)

        # test again with different order of ids
        particles1 = [self.particle_2, self.particle_1, self.particle_1]
        ids1 = list(p.id for p in particles1)
        particles2 = list(p for p in self.pc.iter_particles(ids1))
        self.assertEqual(particles1, particles2)

        self.assertEquals(len(ids1), 3)
        self.assertEquals(len(particles1), len(particles2))
        self.assertEqual(particles1, particles2)
        p_iter = self.pc.iter_particles(ids1)
        particles2 = list(p for p in p_iter)
        p_iter2 = self.pc.iter_particles(ids1)
        particles3 = list(p for p in p_iter2)
        self.assertEqual(particles1, particles2)
        self.assertEqual(particles1, particles3)


if __name__ == '__main__':
    unittest.main()
