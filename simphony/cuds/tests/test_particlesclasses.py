"""
    Testing for particlesclasses module.
"""

import unittest
import uuid

from simphony.cuds.particles import Particle, Bond, ParticleContainer
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA


class ParticleTestCase(unittest.TestCase):
    """Test case for Particle class."""

    def test_simple_particle_default(self):
        particle = Particle()
        self.assertIsInstance(particle, Particle)
        self.assertEqual(particle.coordinates, (0, 0, 0))
        self.assertEqual(particle.uid, None)
        self.assertEqual(particle.data, DataContainer())

    def test_simple_particle_custom(self):
        data = DataContainer()
        data[CUBA.RADIUS] = 3.0
        particle = Particle([20.5, 30.5, 40.5], uuid.UUID(int=33), data)
        self.assertIsInstance(particle, Particle)
        self.assertEqual(particle.coordinates, (20.5, 30.5, 40.5))
        self.assertEqual(particle.uid, uuid.UUID(int=33))
        self.assertEqual(particle.data, data)

    def test_str(self):
        particle = Particle()
        total_str = str(particle.uid) + '_' + str(particle.coordinates)
        self.assertEqual(str(particle), total_str)


class BondTestCase(unittest.TestCase):

    def test_simple_bond(self):
        data = DataContainer()
        data[CUBA.RADIUS] = 2.0
        uuids = [uuid.UUID(int=i) for i in range(3)]
        bond = Bond(uuids, uuid.UUID(int=12), data)
        self.assertIsInstance(bond, Bond)
        self.assertEqual(bond.particles, tuple(uuids))
        self.assertEqual(bond.uid,  uuid.UUID(int=12))
        self.assertEqual(bond.particles, tuple(uuids))
        self.assertEqual(bond.data, data)

    def test_expection_when_initializing_with_empty_tuple(self):
        with self.assertRaises(Exception):
            Bond(())

    def test_str(self):
        uuids = [uuid.UUID(int=i) for i in range(3)]
        bond = Bond(particles=uuids)
        total_str = str(bond.uid) + '_' + str(tuple(uuids))
        self.assertEqual(str(bond), total_str)


class ParticleContainerAddParticlesTestCase(unittest.TestCase):
    def setUp(self):
        self.p_list = []
        for i in xrange(10):
            self.p_list.append(Particle([i, i*10, i*100]))
        self.pc = ParticleContainer(name="foo")

    def test_has_particle(self):
        uid = self.pc.add_particle(self.p_list[0])
        self.assertTrue(self.pc.has_particle(uid))
        self.assertFalse(self.pc.has_particle(uuid.UUID(int=1234)))

    def test_add_particle_ok(self):
        ids = [
            self.pc.add_particle(particle) for particle in self.p_list]
        for index, particle in enumerate(self.p_list):
            self.assertTrue(self.pc.has_particle(particle.uid))
            self.assertEqual(particle.uid, ids[index])

    def test_exception_when_adding_particle_twice(self):
        for particle in self.p_list:
            self.pc.add_particle(particle)
        with self.assertRaises(Exception):
            self.pc.add_particle(self.p_list[0])


class ParticleContainerManipulatingParticlesTestCase(unittest.TestCase):
    def setUp(self):
        self.p_list = []
        self.pc = ParticleContainer(name="foo")
        for i in xrange(10):
            particle = Particle([i, i*10, i*100], uid=uuid.UUID(int=i))
            self.p_list.append(particle)
            self.pc.add_particle(particle)

    def test_update_particle(self):
        particle = self.pc.get_particle(self.p_list[1].uid)
        particle.coordinates = (123, 456, 789)
        part_coords = particle.coordinates
        self.pc.update_particle(particle)
        new_particle = self.pc.get_particle(particle.uid)
        self.assertTrue(new_particle is not particle)
        self.assertEqual(particle.uid, new_particle.uid)
        self.assertEqual(part_coords, new_particle.coordinates)
        self.assertEqual(particle.data, new_particle.data)

    def test_exception_when_update_particle_when_wrong_id(self):
        particle = Particle()
        with self.assertRaises(KeyError):
            self.pc.update_particle(particle)

    def test_remove_particle(self):
        particle = self.p_list[0]
        self.pc.remove_particle(particle.uid)
        self.assertFalse(self.pc.has_particle(particle.uid))

    def test_exception_when_removing_particle_with_bad_id(self):
        with self.assertRaises(KeyError):
            self.pc.remove_particle(uuid.UUID(int=23325))

    def test_iter_particles_when_passing_ids(self):
        particle_ids = [p.uid for p in self.p_list[::2]]
        iterated_ids = [
            particle.uid for particle in self.pc.iter_particles(particle_ids)]
        self.assertEqual(particle_ids, iterated_ids)

    def test_iter_all_particles(self):
        particle_ids = [p.uid for p in self.p_list]
        iterated_ids = [
            particle.uid for particle in self.pc.iter_particles()]
        # The order of iteration is not important in this case.
        self.assertItemsEqual(particle_ids, iterated_ids)

    def test_exception_on_iter_particles_when_passing_wrong_ids(self):
        ids = [particle.uid for particle in self.p_list]
        ids.append(uuid.UUID(int=20))
        with self.assertRaises(KeyError):
            for particle in self.pc.iter_particles(ids):
                last_id = particle.uid
                continue
        self.assertEqual(last_id, self.p_list[-1].uid)


class ParticleContainerAddBondsTestCase(unittest.TestCase):
    def setUp(self):
        self.p_list = []
        self.b_list = []
        for i in xrange(10):
            self.b_list.append(
                Bond([
                    uuid.UUID(int=i),
                    uuid.UUID(int=i + 1),
                    uuid.UUID(int=i+2)]))
        self.pc = ParticleContainer(name="foo")

    def test_has_bond(self):
        uid = self.pc.add_bond(self.b_list[0])
        self.assertTrue(self.pc.has_bond(uid))
        self.assertFalse(self.pc.has_bond(uuid.UUID(int=2122)))

    def test_add_bond(self):
        ids = [self.pc.add_bond(bond) for bond in self.b_list]
        for index, bond in enumerate(self.p_list):
            self.assertTrue(self.pc.has_bond(bond.id))
            self.assertEqual(bond.uid, ids[index])

    def test_exception_when_adding_bond_twice(self):
        for bond in self.b_list:
            self.pc.add_bond(bond)
        with self.assertRaises(Exception):
            self.pc.add_bond(self.b_list[0])


class ParticleContainerManipulatingBondsTestCase(unittest.TestCase):
    def setUp(self):
        self.p_list = []
        self.b_list = []
        self.pc = ParticleContainer(name="foo")
        for i in xrange(10):
            self.p_list.append(Particle([i, i*10, i*100]))
            self.b_list.append(Bond([1, 2, 3]))
            self.pc.add_bond(self.b_list[i])

    def test_update_bond(self):
        bond = self.pc.get_bond(self.b_list[1].uid)
        bond.particles = bond.particles[:-1]
        self.pc.update_bond(bond)
        new_bond = self.pc.get_bond(bond.uid)
        self.assertTrue(new_bond is not bond)
        self.assertEqual(bond.uid, new_bond.uid)
        self.assertEqual(bond.particles, new_bond.particles)
        self.assertEqual(bond.data, bond.data)

    def test_exeception_when_updating_bond_with_incorrect_id(self):
        bond = Bond([1, 2])
        with self.assertRaises(KeyError):
            self.pc.update_bond(bond)

    def test_remove_bond(self):
        bond = self.b_list[0]
        self.pc.remove_bond(bond.uid)
        self.assertFalse(self.pc.has_bond(bond.uid))

    def test_exception_removing_bond_with_missing_id(self):
        with self.assertRaises(KeyError):
            self.pc.remove_bond(uuid.UUID(int=12124124))

    def test_iter_bonds_when_passing_ids(self):
        ids = [b.uid for b in self.b_list[::2]]
        iterated_ids = [
            bond.uid for bond in self.pc.iter_bonds(ids)]
        self.assertEqual(ids, iterated_ids)

    def test_iter_all_bonds(self):
        bonds_ids = [b.uid for b in self.b_list]
        iterated_ids = [bond.uid for bond in self.pc.iter_bonds()]
        # The order of iteration is not important in this case.
        self.assertItemsEqual(bonds_ids, iterated_ids)

    def test_exception_on_iter_bonds_when_passing_wrong_ids(self):
        bonds_ids = [bond.uid for bond in self.b_list]
        bonds_ids.append(uuid.UUID(int=20))
        with self.assertRaises(KeyError):
            for bond in self.pc.iter_bonds(bonds_ids):
                last_id = bond.uid
                continue
        self.assertEqual(last_id, self.b_list[-1].uid)


if __name__ == '__main__':
    unittest.main()
