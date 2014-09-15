import unittest
import copy
import os

from simphony.cuds.particle import Particle
from simphony.cuds.bond import Bond
from simphony.io.cuds_file import CudsFile


class _EmptyParticleContainer():

    def iter_particles(self, ids=None):
        return
        yield


class TestFileParticleContainer(unittest.TestCase):

    def setUp(self):
        # create file with empty particle container
        self.file = CudsFile.open('test_file.cuds')
        self.file.add_particle_container("test", _EmptyParticleContainer())
        self.pc = self.file.get_particle_container('test')

        # create two particles (with unique ids)
        self.particle_1 = Particle((0.1, 0.4, 5.0), id=0)
        self.particle_2 = Particle((0.2, 0.45, 50.0), id=1)

        # create two bonds (with unique ids)
        self.bond_1 = Bond((1, 0), id=0)
        self.bond_2 = Bond((0, 1), id=1)

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

    def test_add_get_particle_with_default_id(self):
        p = Particle((1.0, 1.0, 0.0))
        id = self.pc.add_particle(p)
        particle = self.pc.get_particle(id)
        self.assertTrue(particle is not p)
        self.assertEqual(particle.id, id)
        self.assertEqual(particle.coordinates, p.coordinates)

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

    def test_add_get_bond(self):
        self.pc.add_bond(self.bond_1)
        bond = self.pc.get_bond(self.bond_1.id)
        self.assertTrue(bond is not self.bond_1)
        self.assertEqual(bond, self.bond_1)

    def test_add_get_bond_with_default_id(self):
        b = Bond((1, 0))
        id = self.pc.add_bond(b)
        bond = self.pc.get_bond(id)
        self.assertTrue(bond is not b)
        self.assertEqual(bond.id, id)
        self.assertEqual(bond.particles, b.particles)

    def test_add_bond_with_same_id(self):
        self.pc.add_bond(self.bond_1)
        with self.assertRaises(Exception):
            self.pc.add_bond(self.bond_1)

    def test_get_bond_throws(self):
        with self.assertRaises(Exception):
            self.pc.get_bond(0)

    def test_update_bond(self):
        with self.assertRaises(Exception):
            self.pc.update_bond(self.bond_1)

        self.pc.add_bond(self.bond_1)
        self.pc.add_bond(self.bond_2)
        b = copy.deepcopy(self.bond_1)
        b.particles = (1, 1)
        self.pc.update_bond(b)
        updated_b = self.pc.get_bond(b.id)

        self.assertEqual(b, updated_b)
        self.assertNotEqual(b, self.bond_1)

    def test_iter_bonds(self):
        bondsA = [self.bond_1, self.bond_2]
        for bond in bondsA:
            self.pc.add_bond(bond)

        # test iterating bonds without giving ids
        bondsB = list(p for p in self.pc.iter_bonds())

        self.assertEquals(len(bondsA), len(bondsB))
        for bond in bondsA:
            self.assertTrue(bond in bondsB)

        # test iterating bonds by giving ids
        bondsA = [self.bond_1, self.bond_2]
        ids1 = list(p.id for p in bondsA)
        bondsB = list(p for p in self.pc.iter_bonds(ids1))
        self.assertEqual(bondsA, bondsB)

if __name__ == '__main__':
    unittest.main()
