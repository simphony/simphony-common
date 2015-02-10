Simphony-common
===============

The native implementation of the SimPhoNy cuds objects and io code.

.. image:: https://travis-ci.org/simphony/simphony-common.svg?branch=master
   :target: https://travis-ci.org/simphony/simphony-common
   :alt: Build status

.. image:: https://coveralls.io/repos/simphony/simphony-common/badge.svg
   :target: https://coveralls.io/r/simphony/simphony-common
   :alt: Test coverage

.. image:: https://readthedocs.org/projects/simphony/badge/?version=latest
   :target: https://readthedocs.org/projects/simphony/?badge=latest
   :alt: Documentation Status

Repository
----------

Simphony-common is hosted on github: https://github.com/simphony/simphony-common

Requirements
------------

- enum34 >= 1.0.4
- tables >= 3.1.1
- stevedore >= 1.3.0

Optional requirements
~~~~~~~~~~~~~~~~~~~~~

- click >= 3.3
- pyyaml >= 3.11

Documentation requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~

- sphinx >= 1.2.3
- sphinxcontrib-napoleon >= 0.2.10

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

Documentation
-------------

To build the documentation in the doc/build directory run::

    python setup.py sphinx_build

.. note::

   One can use the --help option with a setup.py command
   to see all available options.

Directory structure
-------------------

There are four subpackages:

- core -- used for common low level classes and utility code
- cuds -- to hold all the native cuds implementations
- io -- to hold the io specific code
- bench -- holds basic benchmarking code
- examples -- holds SimPhoNy example code
- doc -- Documentation related files
  - source -- Sphinx rst source files
  - build -- Documentation build directory, if documentation
    has been generated.
