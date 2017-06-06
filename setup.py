import os
import contextlib
import textwrap
from subprocess import check_call, CalledProcessError

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()

# Setup version
VERSION = '0.7.0.dev0'


@contextlib.contextmanager
def cd(path):
    """Change directory and returns back to cwd once the operation is done."""
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


class Build(build_py):
    def run(self):
        ontology_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "ontology")

        if not os.path.exists(ontology_dir):
            print("Cannot find ontology dir files in {}".format(ontology_dir))
            raise RuntimeError("Unrecoverable error.")

        print("Building classes from ontology")
        cmd_args = ["simphony-meta-generate",
                    ontology_dir,
                    "simphony",
                    "--overwrite"]
        check_call(cmd_args)

        print("Running yapf to reformat in pep8 style")
        cmd_args = ["yapf", "--style", "pep8", "--in-place"]
        try:
            check_call(cmd_args + ["simphony/core/cuba.py"])
            check_call(cmd_args + ["simphony/core/keywords.py"])
            check_call(cmd_args + ["--recursive", "simphony/cuds/meta/"])
        except OSError:
            print(textwrap.dedent("""
                Failed to run yapf. Make sure it is installed in your
                python environment, by running

                pip install yapf
                """))
            raise
        build_py.run(self)


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
        "enum34 >= 1.0.4",
        "stevedore >= 1.2.0",
        "numpy ~= 1.12",
        ],
    extras_require={
        'H5IO': ["tables ~= 3.2.3.1"],
        'CUBAGen': []},
    packages=find_packages(),
    cmdclass={
        'build_py': Build,
    },
    )
