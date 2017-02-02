import unittest
from six import StringIO

from scripts.cuba_enum_generator import CUBAEnumGenerator
from scripts.tests import fixtures


class TestCUBAEnumGenerator(unittest.TestCase):
    def setUp(self):
        self.ontology = fixtures.trivial_ontology

    def test_basic_parsing(self):
        generator = CUBAEnumGenerator()
        output = StringIO()
        generator.generate(self.ontology, output)

        text = output.getvalue()
        for keyword in ["CUBA_DATA_ONE", "CUBA_DATA_TWO", "CUDS_C1",
                        "CUDS_C2", "CUDS_ROOT"]:

            self.assertIn(
                '{keyword} = "{keyword}"'.format(
                    keyword=keyword), text)
