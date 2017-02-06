from __future__ import print_function
import unittest
from six import StringIO
import difflib

from scripts.single_meta_class_generator import SingleMetaClassGenerator
from . import fixtures


class TestSingleMetaClassGenerator(unittest.TestCase):
    def setUp(self):
        self.ontology = fixtures.trivial_ontology()
        self.complex_ontology = fixtures.complex_ontology()

    def test_basic_creation(self):
        generator = SingleMetaClassGenerator()

        output = StringIO()

        generator.generate(self.ontology.root_cuds_item.children[0], output)

        s = output.getvalue()
        self.assertIn("class CUDSC1(CUDSRoot):", s)
        self.assertIn("cuba_key = CUBA.CUDS_C1", s)

    def test_complex_ontology(self):
        generator = SingleMetaClassGenerator()
        output = StringIO()
        cuds_item = self.complex_ontology.root_cuds_item
        gravity_model = cuds_item.children[0].children[0].children[0]

        generator.generate(gravity_model, output)

        expected_output = fixtures.complex_ontology_output_gravity_model()
        obtained_output = output.getvalue()

        if expected_output != obtained_output:
            diff = difflib.ndiff(obtained_output, expected_output)
            print(diff)
            self.fail("expected output and obtained output are different")
