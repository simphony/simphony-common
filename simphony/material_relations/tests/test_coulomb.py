import unittest

from simphony.core.cuba import CUBA
from simphony.material_relations.coulomb import Coulomb
from simphony.testing.abc_check_material_relation import (
    CheckMaterialRelation)


class TestCoulombMaterialRelation(
    CheckMaterialRelation,
    unittest.TestCase
):
    def container_factory(self, name="Coulomb"):
        return Coulomb(
            name=name,
            materials=[0, 1]
        )

    def get_name(self):
        return "Coulomb"

    def get_kind(self):
        return CUBA.COULOMB
if __name__ == '__main__':
    unittest.main()
