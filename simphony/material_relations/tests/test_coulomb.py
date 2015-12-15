import unittest

from simphony.core.cuba import CUBA
from simphony.material_relations.coulomb import Coulomb
from simphony.testing.abc_check_material_relation import (
    CheckMaterialRelation)


class TestCoulombMaterialRelation(
    CheckMaterialRelation,
    unittest.TestCase
):
    def container_factory(
        self,
        name="Coulomb",
        materials=[UUID('66eccff4-d0b2-409f-89ad-c5d2fddfff5e')]  # noqa
    ):
        return Coulomb(
            name=name,
            materials=materials
        )

    def get_name(self):
        return "Coulomb"

    def get_kind(self):
        return CUBA.COULOMB

    def test_cutoff_distance(self):
        relation = self.container_factory('foo_relation')

        self.assertEqual(relation.cutoff_distance, 1.0)

    def test_cutoff_distance_update(self):
        relation = self.container_factory('foo_relation')

        original = relation.cutoff_distance
        relation.cutoff_distance = original + 1

        self.assertEqual(relation.cutoff_distance, original + 1)

    def test_dielectric_contance(self):
        relation = self.container_factory('foo_relation')

        self.assertEqual(relation.dielectric_contance, 1.0)

    def test_dielectric_contance_update(self):
        relation = self.container_factory('foo_relation')

        original = relation.dielectric_contance
        relation.dielectric_contance = original + 1

        self.assertEqual(relation.dielectric_contance, original + 1)

if __name__ == '__main__':
    unittest.main()
