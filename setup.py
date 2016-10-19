import os
import textwrap
from subprocess import check_call

from setuptools import setup, find_packages
from distutils.cmd import Command
from distutils.command.build import build

# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()

# Setup version
VERSION = '0.3.1.dev0'


class BuildMeta(Command):
    def initialize_options(self):
        self.simphony_metadata_path = None

    def finalize_options(self):
        if self.simphony_metadata_path is None:
            check_call([
                "git",
                "clone",
                "https://github.com/simphony/simphony-metadata/"])
            self.simphony_metadata_path = os.path.join(
                os.getcwd(),
                "simphony-metadata/")

    def run(self):
        metadata_yml = os.path.join(
            self.simphony_metadata_path,
            "yaml_files",
            "simphony_metadata.yml")
        cuba_yml = os.path.join( self.simphony_metadata_path,
            "yaml_files",
            "cuba.yml")

        if not (os.path.exists(cuba_yml) and os.path.exists(metadata_yml)):
            print (textwrap.dedent("""
                Cannot open simphony-metadata YAML files.
                Please specify an appropriate path to the simphony-metadata
                git repository in setup.cfg:

                [build]
                simphony_metadata_path=path/to/simphony-metadata-repo/
                """))
            raise

        with open(metadata_yml, 'rb') as simphony_metadata:
            from scripts.generate import meta_class
            meta_class.callback(simphony_metadata, "simphony/cuds/meta/", True)

        with open(metadata_yml, 'rb') as simphony_metadata, \
             open(cuba_yml, 'rb') as cuba, \
             open("simphony/core/keywords.py", "wb") as keywords_out:

            from scripts.generate import keywords
            keywords.callback(cuba, simphony_metadata, keywords_out)

        with open(metadata_yml, 'rb') as simphony_metadata, \
             open(cuba_yml, 'rb') as cuba, \
             open("simphony/core/cuba.py", "wb") as cuba_out:

            from scripts.generate import cuba_enum
            cuba_enum.callback(cuba, simphony_metadata, cuba_out)

        cmd_args = ["yapf", "--style", "pep8", "--in-place"]
        try:
            check_call(cmd_args + ["simphony/core/keywords.py"])
            check_call(cmd_args + ["simphony/core/keywords.py"])
            check_call(cmd_args + ["--recursive", "simphony/cuds/meta/"])
        except OSError as e:
            print (textwrap.dedent("""
                Failed to run yapf. Make sure it is installed in your
                python environment, by running

                pip install yapf
                """)
            )
            raise


class CustomBuild(build):
    sub_commands = build.sub_commands + [
        ('build_meta', None)
    ]




def write_version_py(filename=None):
    if filename is None:
        filename = os.path.join(
            os.path.dirname(__file__), 'simphony', 'version.py')
    ver = """\
version = '%s'
"""
    fh = open(filename, 'wb')
    try:
        fh.write(ver % VERSION)
    finally:
        fh.close()
write_version_py()

# main setup configuration class
setup(
    name='simphony',
    version=VERSION,
    author='SimPhoNy, EU FP7 Project (Nr. 604005) www.simphony-project.eu',
    description='The native implementation of the SimPhoNy cuds objects',
    long_description=README_TEXT,
    install_requires=[
        "enum34>=1.0.4",
        "stevedore>=1.2.0",
        "numpy>=1.4.1"],
    extras_require={
        'H5IO': ["tables>=3.1.1"],
        'CUBAGen': ["click >= 3.3", "pyyaml >= 3.11"]},
    packages=find_packages(),
    cmdclass={
        'build_meta': BuildMeta,
        'build': CustomBuild,
    },
    entry_points={
        'console_scripts': [
            ('simphony-meta-generate = '
             'scripts.generate:cli')]},
    )
