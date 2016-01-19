import unittest
import uuid

from simphony.cuds.material_relations.dissipation_force import (
    DissipationForce)
from simphony.testing.abc_check_material_relation import (
    CheckMaterialRelation)


class TestDissipationForceMaterialRelation(
    CheckMaterialRelation,
    unittest.TestCase
):
    def container_factory(
        self,
            name="DissipationForce",
            materials=[uuid.uuid4() for _ in xrange(1)]):
        return DissipationForce(
            name=name,
            materials=materials
        )

    def test_restitution_coefficient(self):
        relation = self.container_factory('foo_relation')

        self.assertEqual(relation.restitution_coefficient, 1.0)

    def test_restitution_coefficient_update(self):
        relation = self.container_factory('foo_relation')

        original = relation.restitution_coefficient
        relation.restitution_coefficient = original + 1

        self.assertEqual(relation.restitution_coefficient, original + 1)

if __name__ == '__main__':
    unittest.main()
