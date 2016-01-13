import unittest
import uuid

from simphony.cuds.material_relations.coulomb import (
    Coulomb)
from simphony.testing.abc_check_material_relation import (
    CheckMaterialRelation)


class TestCoulombMaterialRelation(
    CheckMaterialRelation,
    unittest.TestCase
):
    def container_factory(
        self,
            name="Coulomb",
            materials=[uuid.uuid4() for _ in xrange(1)]):
        return Coulomb(
            name=name,
            materials=materials
        )

    def test_cutoff_distance(self):
        relation = self.container_factory('foo_relation')

        self.assertEqual(relation.cutoff_distance, 1.0)

    def test_cutoff_distance_update(self):
        relation = self.container_factory('foo_relation')

        original = relation.cutoff_distance
        relation.cutoff_distance = original + 1

        self.assertEqual(relation.cutoff_distance, original + 1)

    def test_dielectric_constant(self):
        relation = self.container_factory('foo_relation')

        self.assertEqual(relation.dielectric_constant, 1.0)

    def test_dielectric_constant_update(self):
        relation = self.container_factory('foo_relation')

        original = relation.dielectric_constant
        relation.dielectric_constant = original + 1

        self.assertEqual(relation.dielectric_constant, original + 1)

if __name__ == '__main__':
    unittest.main()
