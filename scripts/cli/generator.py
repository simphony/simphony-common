from __future__ import print_function

import yaml
import click

from scripts.cuba_enum_generator import CUBAEnumGenerator
from scripts.keywords_generator import KeywordsGenerator
from scripts.meta_class_generator import MetaClassGenerator


@click.group()
def cli():
    """ Auto-generate code from simphony-metadata yaml description. """


@cli.command()
@click.argument('yaml_file', type=click.File('rb'))
@click.argument('out_path', type=click.Path())
@click.option('-O', '--overwrite', is_flag=True, default=False,
              help='Overwrite OUT_PATH')
def meta_class(yaml_file, out_path, overwrite):
    """ Create the Simphony Metadata classes

    YAML_FILE  - path to the simphony_metadata yaml file

    OUT_PATH   - path to the directory where the output files should be placed
    """
    simphony_metadata_dict = yaml.safe_load(yaml_file)

    generator = MetaClassGenerator()
    generator.generate(simphony_metadata_dict, out_path, overwrite)


@cli.command()
@click.argument('cuba_input', type=click.File('rb'))
@click.argument('cuds_input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def cuba_enum(cuba_input, cuds_input, output):
    """ Create the CUBA Enum

    CUBA_INPUT  - Path to the cuba.yml

    CUDS_INPUT  - Path to the simphony_metadata.yml

    OUTPUT      - Path to the output cuba.py file
    """
    cuba_dict = yaml.safe_load(cuba_input)
    simphony_metadata_dict = yaml.safe_load(cuds_input)

    generator = CUBAEnumGenerator()
    generator.generate(cuba_dict, simphony_metadata_dict, output)


@cli.command()
@click.argument('cuba_input', type=click.File('rb'))
@click.argument('cuds_input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def keywords(cuba_input, cuds_input, output):
    """ Create a dictionary of CUDS keywords.

    CUBA_INPUT  - Path to the cuba.yml

    CUDS_INPUT  - Path to the simphony_metadata.yml

    OUTPUT      - Path to the output cuba.py file
    """
    cuba_dict = yaml.safe_load(cuba_input)
    simphony_metadata_dict = yaml.safe_load(cuds_input)
    generator = KeywordsGenerator()
    generator.generate(cuba_dict, simphony_metadata_dict, output)
