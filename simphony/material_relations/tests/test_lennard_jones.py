import unittest

from simphony.core.cuba import CUBA
from simphony.material_relations.lennard_jones import LennardJones
from simphony.testing.abc_check_material_relation import (
    CheckMaterialRelation)


class TestLennardJonesMaterialRelation(
    CheckMaterialRelation,
    unittest.TestCase
):
    def container_factory(self, name="LennardJones"):
        return LennardJones(
            name=name,
            materials=[0, 1]
        )

    def get_name(self):
        return "LennardJones"

    def get_kind(self):
        return CUBA.LENNARD_JONES
if __name__ == '__main__':
    unittest.main()
