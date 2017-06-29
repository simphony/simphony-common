"""Tests for CUDS data structure."""
import uuid
import unittest

from simphony.core import CUBA
from simphony.api import CUDS
from simphony.cuds.meta import api
from simphony.cuds.particles import Particles
from simphony.cuds.particles_items import Particle


class CUDSTestCase(unittest.TestCase):
    """Tests for CUDS container class."""
    def setUp(self):
        self.named_cuds_1 = api.Box(name='mybox')
        self.named_cuds_2 = api.Box(name='mysecondbox')
        self.nameless_cuds_1 = api.Box()

    def test_cuds_uid(self):
        c = CUDS()

        self.assertIsNotNone(c.uid)
        self.assertIsInstance(c.uid, uuid.UUID)

    def test_named_cuds_name(self):
        c = CUDS(name='mycuds')

        self.assertEqual(c.name, 'mycuds')

    def test_nameless_cuds_name(self):
        c = CUDS()

        self.assertIs(c.name, '')

    def test_descriptioned_cuds_description(self):
        c = CUDS(description='test model')

        self.assertEqual(c.description, 'test model')

    def test_descriptionless_cuds_description(self):
        c = CUDS()

        self.assertEqual(c.description, '')

    def test_cuds_data(self):
        c = CUDS()
        data = c.data

        self.assertEqual(c.data, data)
        self.assertIs(c.data, data, msg='data is a copy.')

    def test_add_cuds_component(self):
        c = CUDS()

        self.assertIsNone(c.add([self.named_cuds_1]))
        self.assertIsNone(c.add([self.nameless_cuds_1]))

    def test_add_non_cuds_component(self):
        c = CUDS()

        self.assertRaises(TypeError, c.add, object())

    def test_add_nameless_cuds_component(self):
        c = CUDS()
        c.add([self.nameless_cuds_1])

        self.assertEqual(c.get(self.nameless_cuds_1.uid),
                         self.nameless_cuds_1)
        self.assertRaises(TypeError, c.get_by_name, self.nameless_cuds_1.name)

    def test_add_named_cuds_component(self):
        c = CUDS()

        self.assertIsNone(c.add([self.named_cuds_1]))
        self.assertEqual(c.get_by_name(self.named_cuds_1.name),
                         self.named_cuds_1)

    def test_add_named_component_several_times(self):
        c = CUDS()
        c.add([self.named_cuds_1])

        self.assertRaises(ValueError, c.add, [self.named_cuds_1])

    def test_add_nameless_component_several_times(self):
        c = CUDS()
        c.add([self.nameless_cuds_1])
        c.add([self.nameless_cuds_1])
        component = c.get(self.nameless_cuds_1.uid)

        self.assertEqual(component,
                         self.nameless_cuds_1)
        self.assertRaises(TypeError, c.get_by_name, component.name)

    def test_get_nameless_cuds_component(self):
        c = CUDS()
        c.add([self.nameless_cuds_1])
        component = c.get(self.nameless_cuds_1.uid)

        self.assertEqual(component,
                         self.nameless_cuds_1)
        self.assertRaises(TypeError, c.get_by_name, component.name)

    def test_get_named_cuds_component(self):
        c = CUDS()
        c.add([self.named_cuds_1])

        self.assertEqual(c.get_by_name(self.named_cuds_1.name),
                         self.named_cuds_1)
        self.assertEqual(c.get(self.named_cuds_1.uid),
                         self.named_cuds_1)

    def test_add_named_dataset(self):
        ps = Particles('my particles')
        ps.add([Particle(), Particle()])
        c = CUDS()
        c.add([ps])

        self.assertEqual(c.get_by_name(ps.name), ps)
        self.assertRaises(ValueError, c.add, [ps])

    def test_add_nameless_dataset(self):
        ps = Particles(None)
        ps.add([Particle(), Particle()])
        c = CUDS()

        self.assertRaises(TypeError, c.add, [ps])

    def test_remove_named_component_by_uid(self):
        c = CUDS()
        c.add([self.named_cuds_1])
        c.remove([self.named_cuds_1.uid])

        self.assertRaises(KeyError, c.get_by_name,
                          self.named_cuds_1.name)

    def test_remove_nameless_component_by_uid(self):
        c = CUDS()

        c.add([self.nameless_cuds_1])
        c.remove([self.nameless_cuds_1.uid])

        self.assertRaises(KeyError,
                          c.get,
                          self.nameless_cuds_1.uid)

    def test_remove_dataset(self):
        ps = Particles('my particles')
        ps.add([Particle(), Particle()])
        c = CUDS()
        c.add([ps])
        c.remove([ps.uid])

        self.assertRaises(KeyError, c.get, ps.uid)

    def test_iter_datasets_dimention(self):
        ps1 = Particles('M1')
        ps2 = Particles('M2')
        ps1.add([Particle(), Particle()])
        ps2.add([Particle(), Particle()])

        c = CUDS()
        c.add([ps1])
        c.add([ps2])

        cuds_list = []
        for component in c.iter(item_type=CUBA.PARTICLES):
            cuds_list.append(component)

        self.assertTrue(len(cuds_list), 2)

    def test_iter_datasets_types(self):
        dataset = Particles('M1')
        dataset.add([Particle(),
                     Particle()])
        c = CUDS()
        c.add([dataset])

        for ps in c.iter(item_type=CUBA.PARTICLES):
            self.assertIsInstance(ps, Particles)
            self.assertIn(ps, [dataset])

    def test_iter_with_component(self):
        c = CUDS()

        c.add([self.named_cuds_1])
        c.add([self.named_cuds_2])

        component_list = []
        for component in c.iter(item_type=CUBA.BOX):
            component_list.append(component)

        self.assertTrue(len(component_list), 2)
        for cmp in component_list:
            self.assertIn(cmp, [self.named_cuds_1,
                                self.named_cuds_2])

    def test_iter_with_uid(self):
        c = CUDS()

        c.add([self.named_cuds_1])
        c.add([self.named_cuds_2])

        component_list = []
        for component in c.iter(uids=[self.named_cuds_1.uid]):
            component_list.append(component)

        self.assertTrue(len(component_list), 1)
        self.assertEqual(component_list[0].uid,
                         self.named_cuds_1.uid)

    def test_cuds_update(self):

        component = api.Box(name='a box')
        c = CUDS()
        c.add([component])

        component.name = 'updated box'
        c.update([component])
        updated_component = c.get(component.uid)

        self.assertEqual(updated_component.name, 'updated box')

    def test_cuds_update_invalid_component(self):
        component = api.Box(name='a box')

        c = CUDS()
        c.add([component])

        another_component = api.Box(name='another box')

        with self.assertRaisesRegexp(ValueError, 'Component another box:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12} does not exist') as exc:
            c.update([another_component])

