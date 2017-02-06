import unittest
from six import StringIO

from scripts.single_meta_class_generator import SingleMetaClassGenerator
from . import fixtures


class TestSingleMetaClassGenerator(unittest.TestCase):
    def setUp(self):
        self.ontology = fixtures.trivial_ontology()

    def test_basic_creation(self):
        generator = SingleMetaClassGenerator()

        output = StringIO()

        generator.generate(self.ontology.root_cuds_item.children[0], output)

        print output.getvalue()
