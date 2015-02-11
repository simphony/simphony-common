import copy
import os
import tempfile
import shutil
import unittest

from simphony.cuds.particles import ParticleContainer, Particle, Bond
from simphony.io.h5_cuds import H5CUDS


def _convert_to_tuple_list(particle_or_bond_list):
    converted = []
    for item in particle_or_bond_list:
        if isinstance(item, Particle):
            converted.append((item.uid, item.coordinates))
        elif isinstance(item, Bond):
            converted.append((item.uid, item.particles))
        else:
            raise Exception('unexpected type: %s' % type(item))
    return converted


class TestFileParticleContainer(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        # configure how equality for bond/particles will be tested
        self.addTypeEqualityFunc(Particle, self.assertParticleEqual)
        self.addTypeEqualityFunc(Bond, self.assertBondEqual)

        # create file with empty particle container
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.file = H5CUDS.open(self.filename)
        self.pc = self.file.add_particle_container(
            ParticleContainer(name="test"))

        # create two particles (with unique ids)
        self.particle_1 = Particle((0.1, 0.4, 5.0), uid=0)
        self.particle_2 = Particle((0.2, 0.45, 50.0), uid=1)

        # create two bonds (with unique ids)
        self.bond_1 = Bond((1, 0), uid=0)
        self.bond_2 = Bond((0, 1), uid=1)

    def tearDown(self):
        if os.path.exists(self.filename):
            self.file.close()
        shutil.rmtree(self.temp_dir)

    def compare_list(self, a, b, order_sensitive=True):
        # helper method used to tests lists of
        # particles or bonds
        a = _convert_to_tuple_list(a)
        b = _convert_to_tuple_list(b)
        if order_sensitive:
            self.assertEqual(a, b)
        else:
            self.assertEqual(len(a), len(b))
            for item in a:
                self.assertTrue(item in b)
                b.remove(item)

    def test_add_get_particle(self):
        self.pc.add_particle(self.particle_1)
        particles = self.pc.get_particle(self.particle_1.uid)
        self.assertTrue(particles is not self.particle_1)
        self.assertEqual(particles.uid, self.particle_1.uid)
        self.assertEqual(particles.coordinates, self.particle_1.coordinates)

    def test_add_particle_with_same_id(self):
        self.pc.add_particle(self.particle_1)
        with self.assertRaises(Exception):
            self.pc.add_particle(self.particle_1)

    def test_has_particle_ok(self):
        self.pc.add_particle(self.particle_1)
        self.assertTrue(self.pc.has_particle(self.particle_1.uid))

    def test_has_particle_false(self):
        self.assertFalse(self.pc.has_particle(self.particle_1))

    def test_add_get_particle_with_default_id(self):
        p = Particle((1.0, 1.0, 0.0))
        uid = self.pc.add_particle(p)
        particle = self.pc.get_particle(uid)
        self.assertTrue(particle is not p)
        self.assertEqual(particle.uid, uid)
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
        updated_p = self.pc.get_particle(p.uid)

        self.assertEqual(p, updated_p)
        self.assertNotEqual(p, self.particle_1)

    def test_remove_particle(self):
        with self.assertRaises(ValueError):
            self.pc.remove_particle(0)

        particles = []
        for i in xrange(10):
            particles.append(Particle(
                uid=i, coordinates=(0.0, 0.0, 0.0)))

        for p in particles:
            self.pc.add_particle(p)

        for p in particles:
            self.pc.remove_particle(p.uid)

        for p in particles:
            with self.assertRaises(ValueError):
                self.pc.get_particle(p.uid)

        current = [p for p in self.pc.iter_particles()]
        self.assertFalse(current)

    def test_iter_particles(self):
        particles1 = [self.particle_1, self.particle_2]
        for particle in particles1:
            self.pc.add_particle(particle)

        # test iterating particles without giving ids
        particles2 = list(p for p in self.pc.iter_particles())
        self.compare_list(particles1, particles2, order_sensitive=False)

        # test iterating particles by giving ids
        particles1 = [self.particle_1, self.particle_2]
        ids1 = list(p.uid for p in particles1)
        particles2 = list(p for p in self.pc.iter_particles(ids1))
        self.compare_list(particles1, particles2)

        # test again with different order of ids
        particles1 = [self.particle_2, self.particle_1, self.particle_1]
        ids1 = list(p.uid for p in particles1)
        particles2 = list(p for p in self.pc.iter_particles(ids1))
        self.compare_list(particles1, particles2, order_sensitive=False)

    def test_add_get_bond(self):
        self.pc.add_bond(self.bond_1)
        bond = self.pc.get_bond(self.bond_1.uid)
        self.assertTrue(bond is not self.bond_1)
        self.assertEqual(bond, self.bond_1)

    def test_add_get_bond_with_default_id(self):
        b = Bond((1, 0))
        uid = self.pc.add_bond(b)
        bond = self.pc.get_bond(uid)
        self.assertTrue(bond is not b)
        self.assertEqual(bond.uid, uid)
        self.assertEqual(bond.particles, b.particles)

    def test_add_bond_with_same_id(self):
        self.pc.add_bond(self.bond_1)
        with self.assertRaises(Exception):
            self.pc.add_bond(self.bond_1)

    def test_has_bond_ok(self):
        self.pc.add_bond(self.bond_1)
        self.assertTrue(self.pc.has_bond(self.bond_1.uid))

    def test_has_bond_false(self):
        self.assertFalse(self.pc.has_bond(self.bond_1))

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
        updated_b = self.pc.get_bond(b.uid)

        self.assertEqual(b, updated_b)
        self.assertNotEqual(b, self.bond_1)

    def test_remove_bond(self):
        with self.assertRaises(ValueError):
            self.pc.remove_bond(0)

        bonds = []
        for i in xrange(10):
            bonds.append(Bond(uid=i, particles=(0, 0)))

        for bond in bonds:
            self.pc.add_bond(bond)

        for bond in bonds:
            self.pc.remove_bond(bond.uid)

        for bond in bonds:
            with self.assertRaises(ValueError):
                self.pc.get_bond(bond.uid)

    def test_iter_bonds(self):
        bondsA = [self.bond_1, self.bond_2]
        for bond in bondsA:
            self.pc.add_bond(bond)

        # test iterating bonds without giving ids
        bondsB = list(p for p in self.pc.iter_bonds())
        self.compare_list(bondsA, bondsB, order_sensitive=False)

        # test iterating bonds by giving ids
        bondsA = [self.bond_1, self.bond_2]
        ids1 = list(p.uid for p in bondsA)
        bondsB = list(p for p in self.pc.iter_bonds(ids1))
        self.compare_list(bondsA, bondsB)

    def assertParticleEqual(self, a, b, msg=None):
        self.assertEqual(a.uid, b.uid)
        self.assertEqual(a.coordinates, b.coordinates)

    def assertBondEqual(self, a, b, msg=None):
        self.assertEqual(a.uid, b.uid)
        self.assertEqual(a.particles, b.particles)

if __name__ == '__main__':
    unittest.main()
