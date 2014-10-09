Simphony-common
===============

The native implementation of the SimPhoNy cuds objects and io code.

.. image:: https://travis-ci.org/simphony/simphony-common.svg?branch=master
    :target: https://travis-ci.org/simphony/simphony-common

Repository
----------

Simphony-common is hosted on github: https://github.com/simphony/simphony-common

Installation
------------

The package requires python 2.7.x, installation is based on setuptools::

    # build and install
    python setup.py install

or::

    # build for in-place development
    python setup.py develop

Testing
-------

To run the full test-suite run::

    python -m unittest discover


Directory structure
-------------------

There are four subpackages:

- core -- used for common low level classes and utility code
- cuds -- to hold all the native cuds implementations
- io -- to hold the io specific code
- bench -- holds basic benchmarking code
