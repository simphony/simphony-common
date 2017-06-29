import os
from subprocess import check_call
from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop


# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()


VERSION = '0.8.0.dev0'


def create_ontology_classes():
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


class Build(build_py):
    def run(self):
        create_ontology_classes()
        build_py.run(self)


class Develop(develop):
    def run(self):
        create_ontology_classes()
        develop.run(self)


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

# We cannot use find_packages because we are generating files during build.
packages = [
    'bench',
    'simphony',
    'bench.tests',
    'simphony.core',
    'simphony.cuds',
    'simphony.engine',
    'simphony.io',
    'simphony.pre_processing',
    'simphony.testing',
    'simphony.tools',
    'simphony.visualisation',
    'simphony.core.tests',
    'simphony.cuds.meta',
    'simphony.cuds.tests',
    'simphony.engine.tests',
    'simphony.io.tests',
    'simphony.pre_processing.tests',
    'simphony.testing.tests',
    'simphony.tools.tests',
    'simphony.visualisation.tests'
]

# main setup configuration class
setup(
    name='simphony',
    version=VERSION,
    author='SimPhoNy, EU FP7 Project (Nr. 604005) www.simphony-project.eu',
    description='The native implementation of the SimPhoNy cuds objects',
    long_description=README_TEXT,
    install_requires=[
        "simphony_metatools >= 0.2.0",
        "enum34 >= 1.0.4",
        "stevedore >= 1.2.0",
        "numpy >= 1.11",
        "tables >= 3.2.3.1",
    ],
    extras_require={
        'H5IO': [],
        'CUBAGen': []},
    packages=packages,
    cmdclass={
        'build_py': Build,
        'develop': Develop,
    })
