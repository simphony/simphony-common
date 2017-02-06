from __future__ import print_function

import os

from simphony_metaparser.utils import traverse

from .single_meta_class_generator import SingleMetaClassGenerator
from . import utils


class MetaClassGenerator(object):
    def generate(self, ontology, output_dir):
        """
        Create the Simphony Metadata classes in the directory specified by
        output_dir, from the ontology elements.
        """

        for item, _ in traverse(ontology.root_cuds_item):
            gen = SingleMetaClassGenerator()

            filename = os.path.join(
                output_dir,
                "{}.py".format(utils.cuba_key_to_meta_class_module_name(
                    item.name)))

            # Now write the code
            with open(filename, 'wb') as generated_file:
                gen.generate(item, generated_file)

        # Create an empty __init__.py
        init_path = os.path.join(output_dir, '__init__.py')
        with open(init_path, 'a'):
            pass
