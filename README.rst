Simphony-common
===============

The native implementation of the SimPhoNy cuds objects and io code (http://www.simphony-project.eu/).

.. image:: https://travis-ci.org/simphony/simphony-common.svg?branch=master
   :target: https://travis-ci.org/simphony/simphony-common
   :alt: Build status

.. image:: https://coveralls.io/repos/simphony/simphony-common/badge.svg
   :target: https://coveralls.io/r/simphony/simphony-common
   :alt: Test coverage

.. image:: https://readthedocs.org/projects/simphony/badge/?version=master
   :target: https://readthedocs.org/projects/simphony/?badge=master
   :alt: Documentation Status

Repository
----------

Simphony-common is hosted on github: https://github.com/simphony/simphony-common

Requirements
------------

- enum34 >= 1.0.4
- stevedore >= 1.2.0
- numpy >= 1.4.1

Optional requirements
~~~~~~~~~~~~~~~~~~~~~

To support the cuba-generate script the following packages need to be installed
prior to installing Simphony:

- click >= 3.3
- pyyaml >= 3.11
- tabulate >= 0.7.4

To support the HDF5 based native IO:

- PyTables >= 3.1.1

To support the documentation built you need the following packages:

- sphinx >= 1.2.3
- sphinxcontrib-napoleon >= 0.2.10
- mock

.. note::

  Packages that depend on the optional features and use setuptools should
  append the ``H5IO`` and/or ``CUBAGen`` identifier next to
  simphony in their ``setup_requires`` configuration option. For example::

    install_requires = ["simphony[H5IO, CUBAGen]"]

  Will make sure that the requirements of H5IO and CUBAGen support
  are installed. (see `setuptools extras`_ for more information)

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

    python setup.py build_sphinx


If you recreate the uml diagrams you need to have java and xdot installed::

   sudo apt-get install default-jre xdot

A copy of the `plantuml.jar
<http://plantuml.sourceforge.net/download.html>`_ needs also to be
available in the :file:`doc/` folder. Running ``make uml`` inside
the :file:`doc/` directory will recreate all the UML diagrams.


.. note::

   - One can use the --help option with a setup.py command
     to see all available options.
   - The documentation will be saved in the :file:`./build` directory.
   - Not all the png files of the UML diagrams are used.

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
  - build -- Documentation build directory, if documentation has been generated
    using the ``make`` script in the ``doc`` directory.

SimPhoNy Framework
------------------

The ``simphony`` library is the core component of the SimPhoNy
Framework, infromation on setting up the framework are provided on a
separate repository https://github.com/simphony/simphony-framework.


.. _setuptools extras: https://pythonhosted.org/setuptools/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies
