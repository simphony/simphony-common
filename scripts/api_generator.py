from __future__ import print_function

import os
from scripts.utils import to_camel_case


class APIGenerator(object):
    def generate(self, simphony_metadata_dict, out_path):
        """
        Generates the api.py with the appropriate imports.
        The imports are alphabetically ordered.
        """

        for key in sorted(simphony_metadata_dict['CUDS_KEYS'].keys()):
            with open(os.path.join(out_path, "api.py"), 'ab') as api_file:
                print(
                    'from .{} import {}   # noqa'.format(
                        key.lower(),
                        to_camel_case(key)
                    ),
                    sep='\n',
                    file=api_file
                )
