import unittest
import uuid
from functools import partial

from simphony.cuds.particles import Particle, Bond, Particles
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from simphony.testing.utils import compare_data_containers
from simphony.testing.abc_check_particles import (
    ContainerManipulatingBondsCheck, ContainerAddParticlesCheck,
    ContainerAddBondsCheck, ContainerManipulatingParticlesCheck)


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


class TestNativeContainerAddParticles(
        ContainerAddParticlesCheck, unittest.TestCase):

    def supported_cuba(self):
        return set(CUBA)

    def container_factory(self, name):
        return Particles(name=name)


class TestNativeContainerManipulatingParticles(
        ContainerManipulatingParticlesCheck, unittest.TestCase):

    def supported_cuba(self):
        return set(CUBA)

    def container_factory(self, name):
        return Particles(name=name)


class TestNativeContainerAddBonds(
        ContainerAddBondsCheck, unittest.TestCase):

    def supported_cuba(self):
        return set(CUBA)

    def container_factory(self, name):
        return Particles(name=name)


class TestNativeContainerManipulatingBonds(
        ContainerManipulatingBondsCheck, unittest.TestCase):

    def supported_cuba(self):
        return set(CUBA)

    def container_factory(self, name):
        return Particles(name=name)


class TestParticlesDataContainer(unittest.TestCase):

    def supported_cuba(self):
        return set(CUBA)

    def setUp(self):
        self.addTypeEqualityFunc(
            DataContainer, partial(compare_data_containers, testcase=self))

    def test_data(self):
        pc = Particles(name='foo')
        data = pc.data
        data[CUBA.MASS] = 9
        pc.data = data
        ret_data = pc.data
        self.assertEqual(data, ret_data)
        self.assertIsNot(data, ret_data)
        cur_data = pc.data
        cur_data[CUBA.MASS] = 10
        ret_data = pc.data
        self.assertEqual(data, ret_data)
        self.assertIsNot(data, ret_data)

if __name__ == '__main__':
    unittest.main()
