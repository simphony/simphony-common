"""Tests for CUDS data structure."""
import unittest
import uuid

from simphony import CUDS
from simphony.cuds.particles import Particle, Particles


class CUDSTestCase(unittest.TestCase):
    """CUDS class tests."""
    def setUp(self):
        self.cuds = CUDS()

        # TODO: use generated components
        class DummyComponent(object):
            def __init__(self):
                self.uuid = uuid.uuid4()
                self.name = 'dummyname'
                self.data = {}
        self.dummpy_component1 = DummyComponent()
        self.dummpy_component2 = DummyComponent()

    def test_empty_cuds(self):
        self.assertEqual(len(self.cuds.data), 0)
        self.assertEqual(self.cuds.get('nonexistentkey'), None)
        self.assertEqual(self.cuds.data, {})
        self.assertRaises(KeyError, self.cuds.remove, 'nonexistentkey')

    def test_data(self):
        data = self.cuds.data
        self.assertEqual(self.cuds.data, data)
        self.assertIsNot(self.cuds.data, data)

    def test_add_get_component(self):
        self.assertRaises(TypeError, self.cuds.add, object())
        self.cuds.add(self.dummpy_component1)
        self.assertEqual(self.cuds.get(self.dummpy_component1.uuid),
                         self.dummpy_component1)

    def test_add_dataset(self):
        p1 = Particle()
        p2 = Particle()
        ps = Particles('my particles')
        ps.add_particles([p1, p2])

        self.cuds.add(ps)
        self.assertEqual(self.cuds.get(ps.name), ps)

    def test_remove_component(self):
        self.cuds.add(self.dummpy_component1)
        self.cuds.remove(self.dummpy_component1.uuid)
        self.assertIsNone(self.cuds.get(self.dummpy_component1.uuid))

    def test_remove_dataset(self):
        p1 = Particle()
        p2 = Particle()
        ps = Particles('my particles')
        ps.add_particles([p1, p2])
        self.cuds.add(ps)
        self.cuds.remove(ps.name)
        self.assertIsNone(self.cuds.get(ps.name))

    def test_get_names(self):
        p1 = Particle()
        p2 = Particle()
        p3 = Particle()
        p4 = Particle()
        ps1 = Particles('M1')
        ps2 = Particles('M2')
        ps1.add_particles([p1, p2])
        ps2.add_particles([p3, p4])
        self.cuds.add(ps1)
        self.cuds.add(ps2)
        self.assertEqual(self.cuds.get_names(Particles), ['M1', 'M2'])

        self.cuds.add(self.dummpy_component1)
        self.cuds.add(self.dummpy_component2)
        self.assertEqual(self.cuds.get_names(type(self.dummpy_component1)),
                         [self.dummpy_component1.name,
                          self.dummpy_component2.name])

    def test_iter(self):
        p1 = Particle()
        p2 = Particle()
        p3 = Particle()
        p4 = Particle()
        ps1 = Particles('M1')
        ps2 = Particles('M2')
        ps1.add_particles([p1, p2])
        ps2.add_particles([p3, p4])
        self.cuds.add(ps1)
        self.cuds.add(ps2)
        for item in self.cuds.iter(Particles):
            self.assertIn(item, [ps1, ps2])

        self.cuds.add(self.dummpy_component1)
        self.cuds.add(self.dummpy_component2)
        for item in self.cuds.iter(type(self.dummpy_component1)):
            self.assertIn(item, [self.dummpy_component1,
                                 self.dummpy_component2])
