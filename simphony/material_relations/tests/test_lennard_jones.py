import unittest
import uuid

from simphony.core.cuba import CUBA
from simphony.material_relations.lennard_jones import LennardJones
from simphony.testing.abc_check_material_relation import (
    CheckMaterialRelation)


class TestLennardJonesMaterialRelation(
    CheckMaterialRelation,
    unittest.TestCase
):
    def container_factory(
        self,
        name="LennardJones",
        materials=[uuid.uuid4() for _ in xrange(1)]):
        return LennardJones(
            name=name,
            materials=materials
        )

    def get_name(self):
        return "LennardJones"

    def get_kind(self):
        return CUBA.LENNARD_JONES

    def test_cutoff_distance(self):
        relation = self.container_factory('foo_relation')

        self.assertEqual(relation.cutoff_distance, 1.0)

    def test_cutoff_distance_update(self):
        relation = self.container_factory('foo_relation')

        original = relation.cutoff_distance
        relation.cutoff_distance = original + 1

        self.assertEqual(relation.cutoff_distance, original + 1)

    def test_energy_well_depth(self):
        relation = self.container_factory('foo_relation')

        self.assertEqual(relation.energy_well_depth, 1.0)

    def test_energy_well_depth_update(self):
        relation = self.container_factory('foo_relation')

        original = relation.energy_well_depth
        relation.energy_well_depth = original + 1

        self.assertEqual(relation.energy_well_depth, original + 1)

    def test_van_der_waals_radius(self):
        relation = self.container_factory('foo_relation')

        self.assertEqual(relation.van_der_waals_radius, 1.0)

    def test_van_der_waals_radius_update(self):
        relation = self.container_factory('foo_relation')

        original = relation.van_der_waals_radius
        relation.van_der_waals_radius = original + 1

        self.assertEqual(relation.van_der_waals_radius, original + 1)

if __name__ == '__main__':
    unittest.main()
