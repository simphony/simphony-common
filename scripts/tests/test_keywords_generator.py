from six import StringIO

from scripts.keywords_generator import KeywordsGenerator
from . import fixtures
from .base_test_case import BaseTestCase


class TestKeywordsGenerator(BaseTestCase):
    def setUp(self):
        self.ontology = fixtures.trivial_ontology()

    def test_generation(self):
        generator = KeywordsGenerator()
        output = StringIO()

        generator.generate(self.ontology, output)

        self.assertTextEqual(fixtures.trivial_ontology_keywords_output(),
                             output.getvalue())
