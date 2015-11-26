import unittest
import uuid
from functools import partial

from simphony.cuds.materials import Materials
from simphony.cuds.material import Material
from simphony.testing.utils import (compare_material,
                                    create_data_container)


class TestMaterials(unittest.TestCase):
    """Test case for Materials class."""

    def setUp(self):
        self.addTypeEqualityFunc(Material,
                                 partial(compare_material, testcase=self))
        self.materials = Materials()
        self.example_materials = []
        for i in xrange(5):
            self.example_materials.append(
                Material(description="Material {}".format(i),
                         data=create_data_container()))

    def test_add_get_material(self):
        self.materials.add_material(self.example_materials[0])
        self.assertEqual(self.materials.get_material(
            self.example_materials[0].uid),
            self.example_materials[0])

    def test_get_missing_material(self):
        with self.assertRaises(KeyError):
            self.materials.get_material(uuid.uuid4())

    def test_remove_missing_material(self):
        with self.assertRaises(KeyError):
            self.materials.remove_material(uuid.uuid4())

    def test_iter_materials_with_ids(self):
        # given
        material_subset = [material for material in self.example_materials[:2]]
        subset_ids = [material.uid for material in material_subset]
        for material in self.example_materials:
            self.materials.add_material(material)

        # when
        iterated_with_id_materials = [
            material for material in self.materials.iter_materials(
                subset_ids)]

        # then
        for m, r in zip(iterated_with_id_materials, material_subset):
            self.assertEqual(m, r)

        # when
        iterated_all_materials = {material.uid: material for material
                                  in self.materials.iter_materials()}

        # then
        self.assertEqual(len(iterated_all_materials),
                         len(self.example_materials))
        for material in self.example_materials:
            self.assertEqual(material, iterated_all_materials[material.uid])


if __name__ == '__main__':
    unittest.main()
