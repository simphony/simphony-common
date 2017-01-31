from __future__ import print_function

import yaml
import click
import os
import shutil

from scripts.api_generator import APIGenerator
from scripts.cuba_enum_generator import CUBAEnumGenerator
from scripts.keywords_generator import KeywordsGenerator
from scripts.meta_class_generator import MetaClassGenerator
from scripts.validation_generator import ValidationGenerator


@click.command()
@click.argument('yaml_dir', type=click.Path())
@click.argument('module_root_path', type=click.Path())
@click.option('-O', '--overwrite', is_flag=True, default=False,
              help='Overwrite OUT_PATH')
def cli(yaml_dir, module_root_path, overwrite):
    """ Create the Simphony Metadata classes

    yaml_file:
        path to the simphony_metadata yaml file

    module_root_path:
        path to the root directory of the simphony module.
        Output files will be placed in the appropriate locations
        under this module.

    overwrite:
        Allow overwrite of the file.
    """

    meta_class_output = os.path.join(module_root_path, "cuds", "meta")
    keyword_output = os.path.join(module_root_path, "core", "keywords.py")
    cuba_output = os.path.join(module_root_path, "core", "cuba.py")

    if any([os.path.exists(x) for x in [
        meta_class_output, keyword_output, cuba_output]
           ]):
        if overwrite:
            shutil.rmtree(meta_class_output)
            os.remove(keyword_output)
            os.remove(cuba_output)
        else:
            raise OSError('Generated files already present. '
                          'Will not overwrite without --overwrite')

    try:
        os.mkdir(meta_class_output)
    except OSError:
        pass

    cuba_input = os.path.join(yaml_dir, "cuba.yml")
    cuds_input = os.path.join(yaml_dir, "simphony_metadata.yml")

    with open(cuba_input) as f:
        cuba_dict = yaml.safe_load(f)

    with open(cuds_input) as f:
        simphony_metadata_dict = yaml.safe_load(f)

    generator = KeywordsGenerator()
    with open(keyword_output, "wb") as f:
        generator.generate(cuba_dict, simphony_metadata_dict, f)

    generator = CUBAEnumGenerator()
    with open(cuba_output, "wb") as f:
        generator.generate(cuba_dict, simphony_metadata_dict, f)

    meta_class_generator = MetaClassGenerator()
    meta_class_generator.generate(simphony_metadata_dict, meta_class_output)

    api_generator = APIGenerator()
    api_generator.generate(simphony_metadata_dict, meta_class_output)

    validation_generator = ValidationGenerator()
    validation_generator.generate(meta_class_output)
