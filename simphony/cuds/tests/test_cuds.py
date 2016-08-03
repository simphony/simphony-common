"""Tests for CUDS data structure."""
import unittest

from simphony.api import CUDS
from simphony.cuds.meta import api
from simphony.cuds.particles import Particle, Particles


class CUDSTestCase(unittest.TestCase):
    """CUDS class tests."""
    def setUp(self):
        self.cuds = CUDS()

        self.dummy_component1 = api.Box(name='mybox')
        self.dummy_component2 = api.Box(name='mysecondbox')

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
        # Add non-CUDS non-dataset object
        self.assertRaises(TypeError, self.cuds.add, object())
        self.cuds.add(self.dummy_component1)
        self.assertEqual(self.cuds.get_by_uid(self.dummy_component1.uid),
                         self.dummy_component1)
        self.assertEqual(self.cuds.get(self.dummy_component1.name),
                         self.dummy_component1)

    def test_add_duplicate(self):
        self.cuds.add(self.dummy_component1)
        # Name is the same
        self.assertRaises(ValueError, self.cuds.add, self.dummy_component1)
        self.assertRaises(ValueError,
                          self.cuds.add,
                          api.Material(name=self.dummy_component1.name))

    def test_add_dataset(self):
        p1 = Particle()
        p2 = Particle()
        ps = Particles('my particles')
        ps.add_particles([p1, p2])

        self.cuds.add(ps)
        self.assertEqual(self.cuds.get(ps.name), ps)
        self.assertRaises(ValueError, self.cuds.add, ps)

    def test_remove_component(self):
        self.cuds.add(self.dummy_component1)
        self.cuds.remove(self.dummy_component1.name)
        self.assertIsNone(self.cuds.get(self.dummy_component1.name))

        self.cuds.add(self.dummy_component1)
        self.cuds.remove_by_uid(self.dummy_component1.uid)
        self.assertIsNone(self.cuds.get_by_uid(self.dummy_component1.uid))

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

        self.cuds.add(self.dummy_component1)
        self.cuds.add(self.dummy_component2)
        names = set(self.cuds.get_names(type(self.dummy_component1)))
        self.assertEqual(names,
                         set([self.dummy_component1.name,
                              self.dummy_component2.name]))

    def test_iter_with_dataset(self):
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

        cuds_list = []
        for item in self.cuds.iter(Particles):
            cuds_list.append(item)

        self.assertTrue(len(cuds_list), 2)

        for cuds in cuds_list:
            self.assertIsInstance(cuds, Particles)
            self.assertIn(cuds, [ps1, ps2])

    def test_iter_with_component(self):
        self.cuds.add(self.dummy_component1)
        self.cuds.add(self.dummy_component2)

        component_list = []
        for item in self.cuds.iter(type(self.dummy_component1)):
            component_list.append(item)

        self.assertTrue(len(component_list), 2)
        for cmp in component_list:
            self.assertIn(cmp, [self.dummy_component1,
                                self.dummy_component2])
