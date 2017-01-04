from __future__ import print_function

import shutil
import os


class ValidationGenerator(object):
    def generate(self, out_path):
        """
        Generates the validation code file.
        This file is simply copied from the template to the appropriate place
        in out_path.
        """

        local_dir = os.path.dirname(os.path.abspath(__file__))

        validation_template_path = os.path.join(local_dir,
                                                "validation.template")

        shutil.copy(validation_template_path,
                    os.path.join(out_path, "validation.py"))
