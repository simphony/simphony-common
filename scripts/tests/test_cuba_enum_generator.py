from __future__ import print_function
import unittest
from six import StringIO

from scripts.cuba_enum_generator import CUBAEnumGenerator
from simphony_metaparser.nodes import Ontology, CUBADataType, CUDSItem


class TestCUBAEnumGenerator(unittest.TestCase):

    def test_basic_parsing(self):

        ontology = Ontology()
        ontology.data_types.extend([
            CUBADataType(name="CUBA.CUBA_DATA_ONE",
                         type="string"),
            CUBADataType(name="CUBA.CUBA_DATA_TWO",
                         type="string")
        ])
        ontology.root_cuds_item = CUDSItem(name="CUBA.CUDS_ROOT")
        ontology.root_cuds_item.children.extend([
            CUDSItem(name="CUBA.CUDS_C1"),
            CUDSItem(name="CUBA.CUDS_C2")]
        )
        generator = CUBAEnumGenerator()
        output = StringIO()
        generator.generate(ontology, output)

        text = output.getvalue()
        for keyword in ["CUBA_DATA_ONE", "CUBA_DATA_TWO", "CUDS_C1",
                        "CUDS_C2", "CUDS_ROOT"]:

            self.assertIn(
                '{keyword} = "{keyword}"'.format(
                    keyword=keyword), text)
