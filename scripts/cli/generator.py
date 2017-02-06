from __future__ import print_function

import click
import os
import shutil

from simphony_metaparser.yamldirparser import YamlDirParser

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
    api_output = os.path.join(module_root_path, "cuds", "meta", "api.py")
    keyword_output = os.path.join(module_root_path, "core", "keywords.py")
    cuba_output = os.path.join(module_root_path, "core", "cuba.py")

    if any([os.path.exists(x) for x in [
        meta_class_output, keyword_output, cuba_output]
           ]):
        if overwrite:
            try:
                shutil.rmtree(meta_class_output)
                os.remove(keyword_output)
                os.remove(cuba_output)
            except OSError:
                pass
        else:
            raise OSError('Generated files already present. '
                          'Will not overwrite without --overwrite')

    try:
        os.mkdir(meta_class_output)
    except OSError:
        pass

    parser = YamlDirParser()
    ontology = parser.parse(yaml_dir)

    generator = KeywordsGenerator()
    with open(keyword_output, "wb") as f:
        generator.generate(ontology, f)

    generator = CUBAEnumGenerator()
    with open(cuba_output, "wb") as f:
        generator.generate(ontology, f)

    meta_class_generator = MetaClassGenerator()
    meta_class_generator.generate(ontology, meta_class_output)

    api_generator = APIGenerator()
    with open(api_output, "wb") as f:
        api_generator.generate(ontology, f)

    validation_generator = ValidationGenerator()
    validation_generator.generate(meta_class_output)
