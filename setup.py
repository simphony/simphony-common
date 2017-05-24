import os

from setuptools import setup, find_packages

# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()

# Setup version
VERSION = '0.4.0'


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
        "numpy>=1.12"],
    extras_require={
        'H5IO': ["tables>=3.2.3.1"],
        'CUBAGen': ["click >= 3.3", "pyyaml >= 3.11"]},
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cuba-generate = simphony.scripts.cuba_generate:cli [CUBAGen]']},
    )
