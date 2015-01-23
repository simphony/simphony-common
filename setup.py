import os

from setuptools import setup, find_packages

with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()

VERSION = '0.0.1dev'


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

setup(
    name='simphony',
    version=VERSION,
    author='SimPhoNy FP7 European Project',
    description='The native implementation of the SimPhoNy cuds objects',
    long_description=README_TEXT,
    install_requires=[
        "cython",
        "enum34",
        "tables",
        "click",
        "pyyaml"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cuba-generate = simphony.scripts.cuba_generate:cli']
    })
