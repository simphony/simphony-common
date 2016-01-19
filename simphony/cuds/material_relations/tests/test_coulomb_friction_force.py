import unittest
import uuid

from simphony.cuds.material_relations.coulomb_friction_force import (
    CoulombFrictionForce)
from simphony.testing.abc_check_material_relation import (
    CheckMaterialRelation)


class TestCoulombFrictionForceMaterialRelation(
    CheckMaterialRelation,
    unittest.TestCase
):
    def container_factory(
        self,
            name="CoulombFrictionForce",
            materials=[uuid.uuid4() for _ in xrange(1)]):
        return CoulombFrictionForce(
            name=name,
            materials=materials
        )

    def test_friction_coefficient(self):
        relation = self.container_factory('foo_relation')

        self.assertEqual(relation.friction_coefficient, 0.0)

    def test_friction_coefficient_update(self):
        relation = self.container_factory('foo_relation')

        original = relation.friction_coefficient
        relation.friction_coefficient = original + 1

        self.assertEqual(relation.friction_coefficient, original + 1)

if __name__ == '__main__':
    unittest.main()
