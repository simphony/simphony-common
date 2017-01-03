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

    if os.path.exists(out_path):
        if overwrite:
            shutil.rmtree(out_path)
        else:
            raise OSError('Destination already exists: {!r}'.format(out_path))

    yml_data = yaml.safe_load(yaml_file)

    all_generators = {}

    # Temporary directory that stores the output
    with make_temporary_directory() as temp_dir:

        for key, class_data in yml_data['CUDS_KEYS'].items():
            # Catch inconsistent definitions that would choke the generator
            parent = class_data['parent']
            if (parent and
                    parent.replace('CUBA.', '') not in yml_data['CUDS_KEYS']):
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
            all_generators[key] = CodeGenerator(key, class_data)

        for key, gen in all_generators.items():
            # Collect parents and attributes inherited from parents
            gen.collect_parents_to_mro(all_generators)
            gen.collect_attributes_from_parents(all_generators)

            # Target .py file
            filename = os.path.join(temp_dir,
                                    "{}.py".format(gen.original_key.lower()))

            # Now write the code
            with open(filename, 'wb') as generated_file:
                gen.generate(file_out=generated_file)

            # Print to the api.py
            with open(os.path.join(temp_dir, "api.py"), 'ab') as api_file:
                print('from .{} import {}   # noqa'.format(key.lower(),
                                                           to_camel_case(key)),
                      sep='\n', file=api_file)

        # Create an empty __init__.py
        init_path = os.path.join(temp_dir, '__init__.py')
        open(init_path, 'a').close()

        # Create validation.py
        validation_path = os.path.join(temp_dir, 'validation.py')

        from .. import validation
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
