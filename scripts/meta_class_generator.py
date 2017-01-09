from __future__ import print_function

import os

from .single_meta_class_generator import SingleMetaClassGenerator
from . import utils


class MetaClassGenerator(object):
    def generate(self, simphony_metadata_dict, out_path):
        """
        Create the Simphony Metadata classes in the directory specified by
        out_path, starting from the yaml-extracted data in
        simphony_metadata_dict.

        If the optional overwrite flag is True, the directory will be
        emptied first.
        """

        for key, class_data in simphony_metadata_dict['CUDS_KEYS'].items():
            gen = SingleMetaClassGenerator(key, simphony_metadata_dict)

            filename = os.path.join(
                out_path,
                "{}.py".format(utils.cuba_key_to_meta_class_module_name(key)))

            # Now write the code
            with open(filename, 'wb') as generated_file:
                gen.generate(out=generated_file)

        # Create an empty __init__.py
        init_path = os.path.join(out_path, '__init__.py')
        open(init_path, 'a').close()
