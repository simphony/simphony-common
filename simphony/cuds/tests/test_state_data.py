import unittest
import uuid
from functools import partial

from simphony.cuds.state_data import StateData
from simphony.cuds.material import Material
from simphony.testing.utils import (compare_material,
                                    create_data_container)


class TestStateData(unittest.TestCase):
    """Test case for StateData class."""

    def setUp(self):
        self.addTypeEqualityFunc(Material,
                                 partial(compare_material, testcase=self))
        self.state_data = StateData()
        self.materials = []
        for i in xrange(5):
            self.materials.append(
                Material(description="Material {}".format(i),
                         data=create_data_container()))

    def test_add_get_material(self):
        self.state_data.add_material(self.materials[0])
        self.assertEqual(self.state_data.get_material(self.materials[0].uid),
                         self.materials[0])

    def test_get_missing_material(self):
        with self.assertRaises(KeyError):
            self.state_data.get_material(uuid.uuid4())

    def test_remove_missing_material(self):
        with self.assertRaises(KeyError):
            self.state_data.remove_material(uuid.uuid4())

    def test_iter_materials_with_ids(self):
        # given
        materials_subset = [material for material in self.materials[:2]]
        subset_ids = [material.uid for material in materials_subset]
        for material in self.materials:
            self.state_data.add_material(material)

        # when
        iterated_with_id_materials = [
            material for material in self.state_data.iter_materials(
                subset_ids)]

        # then
        for m, r in zip(iterated_with_id_materials, materials_subset):
            self.assertEqual(m, r)

        # when
        iterated_all_materials = {material.uid: material for material
                                  in self.state_data.iter_materials()}

        # then
        self.assertEqual(len(iterated_all_materials),
                         len(self.materials))
        for material in self.materials:
            self.assertEqual(material, iterated_all_materials[material.uid])


if __name__ == '__main__':
    unittest.main()
