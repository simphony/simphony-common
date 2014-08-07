simphony-common
===============

The native implementation of the Simphony cuds objects

Repository
----------

Simphony-common is hosted on github: https://github.com/simphony/simphony-common

Installation
------------

The package requires python 2.7.x, installation is based on setuptools::

    # build and install
    python setup.py install

or::

    # build for inplace development
    python setup.py install

Testing
-------

To run the full test-suite run::

    python -m unittest discover


Directory structure
-------------------

There are three subpackages:

- core -- used for common low level classes and utility code
- cuds -- to hold all the native cuds implementations
- io -- to hold the io specific code
