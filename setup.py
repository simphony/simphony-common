import os

from setuptools import setup, find_packages

# Gather additional setup.py commands
try:
    from sphinx.setup_command import BuildDoc
    cmdclass = {'sphinx_build': BuildDoc}
except ImportError:
    print "Sphinx not found documentation building is not available"
    cmdclass = {}

# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()

# Setup version
VERSION = '0.0.1.dev2'


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
    author='SimPhoNy FP7 European Project',
    description='The native implementation of the SimPhoNy cuds objects',
    long_description=README_TEXT,
    install_requires=[
        "enum34>=1.0.4",
        "tables>=3.1.1",
        "stevedore>=1.3.0"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cuba-generate = simphony.scripts.cuba_generate:cli']},
    cmdclass=cmdclass)
