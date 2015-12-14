import unittest

from simphony.core.cuba import CUBA
from simphony.material_relations.lennard_jones import LennardJones
from simphony.testing.abc_check_material_relation import (
    CheckMaterialRelation)


class TestLennardJonesMaterialRelation(
    CheckMaterialRelation,
    unittest.TestCase
):
    def container_factory(self, name):
        return LennardJones(
            materials='[0,1]'
        )

    def get_kind(self):
        return CUBA.LENNARD_JONES
