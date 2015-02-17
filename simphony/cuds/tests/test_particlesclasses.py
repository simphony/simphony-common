import unittest
import uuid
from functools import partial

from simphony.cuds.particles import Particle, Bond, ParticleContainer
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from simphony.io.tests.utils import (
    compare_particles, create_particles, compare_bonds, create_bonds)


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
        self.assertEqual(
            str(Particle()), "uid:None\ncoordinates:(0.0, 0.0, 0.0)\ndata:{}")


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


class AddParticlesTestCase(unittest.TestCase):

    def setUp(self):
        self.particle_list = create_particles()
        self.container = self.container_factory('foo')
        self.ids = [
            self.container.add_particle(particle)
            for particle in self.particle_list]

    def container_factory(self, name):
        return ParticleContainer(name=name)

    def test_has_particle(self):
        container = self.container
        self.assertTrue(container.has_particle(self.ids[6]))
        self.assertFalse(container.has_particle(uuid.UUID(int=1234)))

    def test_add_particle_ok(self):
        container = self.container
        for index, particle in enumerate(self.particle_list):
            self.assertTrue(container.has_particle(particle.uid))
            self.assertEqual(particle.uid, self.ids[index])

    def test_exception_when_adding_particle_twice(self):
        container = self.container
        with self.assertRaises(ValueError):
            container.add_particle(self.particle_list[3])


class ManipulatingParticlesTestCase(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(
            Particle, partial(compare_particles, testcase=self))
        self.maxDiff = None
        self.particle_list = create_particles()
        self.container = self.container_factory('foo')
        self.ids = [
            self.container.add_particle(particle)
            for particle in self.particle_list]

    def container_factory(self, name):
        return ParticleContainer(name=name)

    def test_get_particle(self):
        container = self.container
        for uid, particle in map(None, self.ids, self.particle_list):
            self.assertEqual(container.get_particle(uid), particle)

    def test_update_particle(self):
        container = self.container
        particle = container.get_particle(self.ids[2])
        particle.coordinates = (123, 456, 789)
        container.update_particle(particle)
        retrieved = container.get_particle(particle.uid)
        self.assertEqual(retrieved, particle)

    def test_exception_when_update_particle_when_wrong_id(self):
        container = self.container
        particle = Particle(uid=uuid.uuid4())
        with self.assertRaises(ValueError):
            container.update_particle(particle)
        particle = Particle()
        with self.assertRaises(ValueError):
            container.update_particle(particle)

    def test_remove_particle(self):
        container = self.container
        particle = self.particle_list[0]
        container.remove_particle(particle.uid)
        self.assertFalse(container.has_particle(particle.uid))

    def test_exception_when_removing_particle_with_bad_id(self):
        container = self.container
        with self.assertRaises(KeyError):
            container.remove_particle(uuid.UUID(int=23325))
        with self.assertRaises(KeyError):
            container.remove_particle(None)

    def test_iter_particles_when_passing_ids(self):
        particles = [particle for particle in self.particle_list[::2]]
        ids = [particle.uid for particle in particles]
        iterated_particles = [
            particle for particle in self.container.iter_particles(ids)]
        for particle, reference in map(None, iterated_particles, particles):
            self.assertEqual(particle, reference)

    def test_iter_all_particles(self):
        particles = {particle.uid: particle for particle in self.particle_list}
        iterated_particles = [
            particle for particle in self.container.iter_particles()]
        # The order of iteration is not important in this case.
        self.assertEqual(len(particles), len(iterated_particles))
        for particle in iterated_particles:
            self.assertEqual(particle, particles[particle.uid])

    def test_exception_on_iter_particles_when_passing_wrong_ids(self):
        ids = [particle.uid for particle in self.particle_list]
        ids.append(uuid.UUID(int=20))
        with self.assertRaises(KeyError):
            for particle in self.container.iter_particles(ids):
                pass
        self.assertEqual(particle.uid, self.particle_list[-1].uid)


class AddBondsTestCase(unittest.TestCase):

    def setUp(self):
        self.bond_list = create_bonds()
        self.container = self.container_factory("foo")
        self.ids = [
            self.container.add_bond(bond) for bond in self.bond_list]

    def container_factory(self, name):
        return ParticleContainer(name=name)

    def test_has_bond(self):
        container = self.container
        self.assertTrue(container.has_bond(self.ids[2]))
        self.assertFalse(container.has_bond(uuid.UUID(int=2122)))

    def test_add_bond(self):
        for index, bond in enumerate(self.bond_list):
            self.assertTrue(self.container.has_bond(bond.uid))
            self.assertEqual(bond.uid, self.ids[index])

    def test_exception_when_adding_bond_twice(self):
        with self.assertRaises(ValueError):
            self.container.add_bond(self.bond_list[4])


class ManipulatedBondsTestCase(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(
            Bond, partial(compare_bonds, testcase=self))
        self.bond_list = create_bonds()
        self.container = self.container_factory("foo")
        self.ids = [
            self.container.add_bond(bond) for bond in self.bond_list]

    def container_factory(self, name):
        return ParticleContainer(name=name)

    def test_get_bond(self):
        container = self.container
        for uid, bond in map(None, self.ids, self.bond_list):
            self.assertEqual(container.get_bond(uid), bond)

    def test_update_bond(self):
        container = self.container
        bond = container.get_bond(self.ids[1])
        bond.particles = bond.particles[:-1]
        bond.data = DataContainer()
        container.update_bond(bond)
        new_bond = container.get_bond(bond.uid)
        self.assertEqual(new_bond, bond)
        self.assertNotEqual(new_bond, self.bond_list[1])

    def test_exeception_when_updating_bond_with_incorrect_id(self):
        bond = Bond([1, 2])
        with self.assertRaises(ValueError):
            self.container.update_bond(bond)

    def test_remove_bond(self):
        container = self.container
        uid = self.ids[0]
        container.remove_bond(uid)
        self.assertFalse(self.container.has_bond(uid))

    def test_exception_removing_bond_with_missing_id(self):
        with self.assertRaises(KeyError):
            self.container.remove_bond(uuid.UUID(int=12124124))

    def test_iter_bonds_when_passing_ids(self):
        bonds = [bond for bond in self.bond_list[::2]]
        ids = [bond.uid for bond in bonds]
        iterated_bonds = [
            bond for bond in self.container.iter_bonds(ids)]
        for bond, reference in map(None, iterated_bonds, bonds):
            self.assertEqual(bond, reference)

    def test_iter_all_bonds(self):
        bonds = {bonds.uid: bonds for bonds in self.bond_list}
        iterated_bonds = [
            bond for bond in self.container.iter_bonds()]
        # The order of iteration is not important in this case.
        self.assertEqual(len(bonds), len(bonds))
        for bond in iterated_bonds:
            self.assertEqual(bond, bonds[bond.uid])

    def test_exception_on_iter_bonds_when_passing_wrong_ids(self):
        bonds_ids = self.ids
        bonds_ids.append(uuid.UUID(int=20))
        with self.assertRaises(KeyError):
            for bond in self.container.iter_bonds(bonds_ids):
                pass
        self.assertEqual(bond.uid, self.bond_list[-1].uid)


if __name__ == '__main__':
    unittest.main()
