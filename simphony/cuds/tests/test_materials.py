import unittest
import uuid
from functools import partial

from simphony.cuds import CUDS
from simphony.cuds.meta.api import Material
from simphony.testing.utils import compare_material


class TestMaterials(unittest.TestCase):
    """Test case for Materials class."""

    def setUp(self):
        self.addTypeEqualityFunc(Material,
                                 partial(compare_material, testcase=self))
        self.materials = CUDS()
        self.example_materials = []
        for i in xrange(5):
            m = Material(description="Material {}".format(i))
            m.name = ""
            self.example_materials.append(m)

    def test_add_get_material(self):
        self.materials.add(self.example_materials[0])
        self.assertEqual(self.materials.get_by_uid(
            self.example_materials[0].uid),
            self.example_materials[0])

    def test_add_existing_material(self):
        # Adding the same material has no effect
        self.materials.add(self.example_materials[0])
        self.materials.add(self.example_materials[0])

        # API not there yet...
        # self.assertEqual(self.materials.count_of(Material), 1)

    def test_get_missing_material(self):
        self.assertIsNone(self.materials.get(uuid.uuid4()))

    def test_remove_missing_material(self):
        with self.assertRaises(KeyError):
            self.materials.remove(uuid.uuid4())

    def test_iter_all_materials_with_ids(self):
        # given
        for material in self.example_materials:
            self.materials.add(material)

        # when
        iterated_all_materials = {material.uid: material for material
                                  in self.materials.iter(Material)}

        # then
        self.assertEqual(len(iterated_all_materials),
                         len(self.example_materials))
        for material in self.example_materials:
            self.assertEqual(material, iterated_all_materials[material.uid])

    def test_iter_subset_of_materials_with_ids(self):
        # given
        material_subset = [material for material in self.example_materials[:2]]

        subset_ids = [material.uid for material in material_subset]
        for material in self.example_materials:
            self.materials.add(material)

        # when
        iterated_materials = {material.uid: material for material
                              in self.materials.iter(Material)
                              if material.uid in subset_ids}

        # then
        self.assertEqual(len(iterated_materials),
                         len(material_subset))
        for material in material_subset:
            self.assertEqual(material, iterated_materials[material.uid])


if __name__ == '__main__':
    unittest.main()
