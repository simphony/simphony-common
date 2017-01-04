from __future__ import print_function

import shutil
import os
import warnings
import re

from scripts.single_meta_class_generator import (
    SingleMetaClassGenerator, IMPORT_PATHS)
from scripts.utils import make_temporary_directory, to_camel_case


class MetaClassGenerator(object):
    def generate(self, simphony_metadata_dict, out_path, overwrite=True):
        """
        Create the Simphony Metadata classes in the directory specified by
        out_path, starting from the yaml-extracted data in
        simphony_metadata_dict.

        If the optional overwrite flag is True, the directory will be
        emptied first.
        """

        if os.path.exists(out_path):
            if overwrite:
                shutil.rmtree(out_path)
            else:
                raise OSError('Destination already exists: {!r}'.format(
                    out_path))

        all_generators = {}

        # Temporary directory that stores the output
        with make_temporary_directory() as temp_dir:

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
                    temp_dir,
                    "{}.py".format(gen.original_key.lower()))

                # Now write the code
                with open(filename, 'wb') as generated_file:
                    gen.generate(file_out=generated_file)

                # Print to the api.py
                with open(os.path.join(temp_dir, "api.py"), 'ab') as api_file:
                    print(
                        'from .{} import {}   # noqa'.format(
                            key.lower(),
                            to_camel_case(key)
                        ),
                        sep='\n',
                        file=api_file
                    )

            # Create an empty __init__.py
            init_path = os.path.join(temp_dir, '__init__.py')
            open(init_path, 'a').close()

            # Create validation.py
            validation_path = os.path.join(temp_dir, 'validation.py')

            from . import validation
            # validation.py for validation codes.
            validation_py_path = os.path.splitext(validation.__file__)[0]+'.py'

            with open(validation_path, 'wb') as dst_file, \
                    open(validation_py_path, 'rb') as src_file:

                # Replace import path for KEYWORDS
                def read_lines(src_file):
                    while True:
                        line = src_file.next()
                        yield re.sub(r'(\s*).+import KEYWORDS',
                                     "\\1"+IMPORT_PATHS['KEYWORDS'], line)

                # Copy the rest of the file
                print(*read_lines(src_file), file=dst_file, sep='')

            # Copy everything to the output directory
            shutil.copytree(temp_dir, out_path)
