import unittest
import uuid

from simphony.cuds.material_relations.sjkr_cohesion_force import (
    SJKRCohesionForce)
from simphony.testing.abc_check_material_relation import (
    CheckMaterialRelation)


class TestSJKRCohesionForceMaterialRelation(
    CheckMaterialRelation,
    unittest.TestCase
):
    def container_factory(
        self,
            name="SJKRCohesionForce",
            materials=[uuid.uuid4() for _ in xrange(1)]):
        return SJKRCohesionForce(
            name=name,
            materials=materials
        )

    def test_cohesion_energy_density(self):
        relation = self.container_factory('foo_relation')

        self.assertEqual(relation.cohesion_energy_density, 0.0)

    def test_cohesion_energy_density_update(self):
        relation = self.container_factory('foo_relation')

        original = relation.cohesion_energy_density
        relation.cohesion_energy_density = original + 1

        self.assertEqual(relation.cohesion_energy_density, original + 1)

if __name__ == '__main__':
    unittest.main()
