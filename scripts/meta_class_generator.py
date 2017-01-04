from __future__ import print_function

import os
import warnings

from scripts.single_meta_class_generator import SingleMetaClassGenerator


class MetaClassGenerator(object):
    def generate(self, simphony_metadata_dict, out_path):
        """
        Create the Simphony Metadata classes in the directory specified by
        out_path, starting from the yaml-extracted data in
        simphony_metadata_dict.

        If the optional overwrite flag is True, the directory will be
        emptied first.
        """

        all_generators = {}

        for key, class_data in simphony_metadata_dict['CUDS_KEYS'].items():
            # Catch inconsistent definitions that would choke the generator
            parent = class_data['parent']
            if (parent and parent.replace('CUBA.', '')
                    not in simphony_metadata_dict['CUDS_KEYS']):
                message = ('{0} is SKIPPED because its parent {1} '
                           'is not defined in CUDS_KEYS')
                warnings.warn(message.format(key, class_data['parent']))
                continue

            if key.lower() in ('validation', 'api'):
                message = 'Name crashes with utility modules: '+key.lower()
                raise ValueError(message)

            # Create the generator object, on init, it identifies its own
            # required/optional user-defined attributes and
            # system-managed attributes
            all_generators[key] = SingleMetaClassGenerator(key, class_data)

        for key, gen in all_generators.items():
            # Collect parents and attributes inherited from parents
            gen.collect_parents_to_mro(all_generators)
            gen.collect_attributes_from_parents(all_generators)

            # Target .py file
            filename = os.path.join(
                out_path,
                "{}.py".format(gen.original_key.lower()))

            # Now write the code
            with open(filename, 'wb') as generated_file:
                gen.generate(file_out=generated_file)

        # Create an empty __init__.py
        init_path = os.path.join(out_path, '__init__.py')
        open(init_path, 'a').close()
