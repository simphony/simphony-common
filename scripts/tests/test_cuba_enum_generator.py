import unittest
from six import StringIO

from simphony_metaparser.nodes import CUDSItem
from scripts.cuba_enum_generator import CUBAEnumGenerator
from scripts.tests import fixtures


class TestCUBAEnumGenerator(unittest.TestCase):
    def setUp(self):
        self.ontology = fixtures.trivial_ontology()

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

    def test_long_line(self):
        generator = CUBAEnumGenerator()
        output = StringIO()
        self.ontology.root_cuds_item.children.append(
            CUDSItem(
                name="CUBA.REALLY_LONG_NAME_THAT_GOES_BEYOND_THE_79_CHARACTER_LIMIT",  # noqa
                parent=self.ontology.root_cuds_item
                )
            )

        generator.generate(self.ontology, output)

        text = output.getvalue()
        self.assertIn(
            '"REALLY_LONG_NAME_THAT_GOES_BEYOND_THE_79_CHARACTER_LIMIT"  # noqa',  # noqa
            text)
