import unittest
from six import StringIO

from scripts.keywords_generator import KeywordsGenerator
from scripts.tests import fixtures


class TestKeywordsGenerator(unittest.TestCase):
    def setUp(self):
        self.ontology = fixtures.trivial_ontology()

    def test_generation(self):
        generator = KeywordsGenerator()
        output = StringIO()

        generator.generate(self.ontology, output)

        print output.getvalue()


