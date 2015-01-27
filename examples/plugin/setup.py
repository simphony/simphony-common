from setuptools import setup, find_packages

setup(
    name='simphony_plugin_example',
    version='1.0',
    author='SimPhoNy FP7 European Project',
    description='An example plugin package',
    packages=find_packages(),
    entry_points={
        'simphony.visualisation': ['example = simphony_example']
    })
