import unittest
import uuid

from simphony.cuds.particles import Particle, Bond, Particles
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from simphony.testing.abc_check_particles import (
    CheckManipulatingBonds, CheckAddingParticles,
    CheckAddingBonds, CheckManipulatingParticles,
    CheckParticlesContainer)


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

    def test_exception_when_initializing_with_empty_tuple(self):
        with self.assertRaises(Exception):
            Bond(())

    def test_str(self):
        uuids = [uuid.UUID(int=i) for i in range(3)]
        bond = Bond(particles=uuids)
        total_str = str(bond.uid) + '_' + str(tuple(uuids))
        self.assertEqual(str(bond), total_str)


class TestNativeContainerAddingParticles(
        CheckAddingParticles, unittest.TestCase):

    def supported_cuba(self):
        return set(CUBA)

    def container_factory(self, name):
        return Particles(name=name)


class TestNativeContainerManipulatingParticles(
        CheckManipulatingParticles, unittest.TestCase):

    def supported_cuba(self):
        return set(CUBA)

    def container_factory(self, name):
        return Particles(name=name)


class TestNativeContainerAddBonds(CheckAddingBonds, unittest.TestCase):

    def supported_cuba(self):
        return set(CUBA)

    def container_factory(self, name):
        return Particles(name=name)


class TestNativeContainerManipulatingBonds(
        CheckManipulatingBonds, unittest.TestCase):

    def supported_cuba(self):
        return set(CUBA)

    def container_factory(self, name):
        return Particles(name=name)


class TestParticlesContainer(CheckParticlesContainer, unittest.TestCase):

    def supported_cuba(self):
        return set(CUBA)

    def container_factory(self, name):
        return Particles(name=name)


if __name__ == '__main__':
    unittest.main()
