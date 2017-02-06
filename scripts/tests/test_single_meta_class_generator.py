from __future__ import print_function
from six import StringIO

from scripts.single_meta_class_generator import SingleMetaClassGenerator
from .base_test_case import BaseTestCase
from . import fixtures


class TestSingleMetaClassGenerator(BaseTestCase):
    def setUp(self):
        self.ontology = fixtures.trivial_ontology()
        self.complex_ontology = fixtures.complex_ontology()
        self.reimplemented_property_ontology = \
            fixtures.ontology_with_reimplemented_variable_properties()

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

        self.assertTextEqual(fixtures.complex_ontology_output_gravity_model(),
                             output.getvalue())

    def test_ontology_with_reimplemented_property(self):

        generator = SingleMetaClassGenerator()
        output = StringIO()
        cuds_item = self.reimplemented_property_ontology.root_cuds_item

        for _ in range(4):
            cuds_item = cuds_item.children[0]

        generator.generate(cuds_item, output)

        self.assertNotIn("self._init_material(material)", output.getvalue())
        self.assertNotIn("return (CUBA.MATERIAL, )", output.getvalue())
