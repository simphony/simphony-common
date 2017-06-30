Simphony-common
===============

The native implementation of the SimPhoNy cuds objects and io code (http://www.simphony-project.eu/).

.. image:: https://travis-ci.org/simphony/simphony-common.svg?branch=master
   :target: https://travis-ci.org/simphony/simphony-common
   :alt: Build status

.. image:: http://codecov.io/github/simphony/simphony-common/coverage.svg?branch=master
   :target: http://codecov.io/github/simphony/simphony-common?branch=master
   :alt: Coverage status

.. image:: https://readthedocs.org/projects/simphony/badge/?version=master
   :target: https://readthedocs.org/projects/simphony/?badge=master
   :alt: Documentation Status

.. image:: https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg
   :target: https://hub.docker.com/r/simphony/simphony-common/
   :alt: Docker Image

Repository
----------

Simphony-common is hosted on github: https://github.com/simphony/simphony-common

Requirements
------------

- enum34 >= 1.0.4
- stevedore >= 1.2.0
- numpy >= 1.11.1
- PyTables >= 3.2.3.1

Optional requirements
~~~~~~~~~~~~~~~~~~~~~

To support the documentation built you need the following packages:

- sphinx >= 1.3.1
- mock

Installation
------------

The package requires python 2.7.x, installation is based on setuptools::

    # build and install
    python setup.py install

or::

    # build for in-place development
    python setup.py develop

Generation of EDM egg
---------------------

An EDM egg can be generated with::
    
    python edmsetup.py egg

the resulting egg will be left in the endist directory.
Uploading to the repository is only possible from an Enthought jenkins build process.
Automatic build of the eggs is performed when a branch (not a tag, due to jenkins github 
limitations) named ``release-<version>-<build>`` is created. If the build is successful, 
the package will appear in the enthought/simphony-dev repository shortly afterwards.

We recommend to leave these branches for future reference.


Testing
-------

To run the full test-suite run::

    python -m unittest discover -p test*

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
Framework; information on setting up the framework is provided on a
separate repository https://github.com/simphony/simphony-framework.
Observe that this repository is in deprecation stage, as we are moving toward
Enthought Deployment Manager (EDM) based installation and deployment.


For Developers
==============

The data structures used in this project are based on the metadata which is defined under ``ontology``.

In order to reflect latest changes to the metadata repository, one should regenerate these entities. 
The generator is hosted in the repository simphony-metatools located at: https://github.com/simphony/simphony-metatools . The generator is
used to recreate the python classes in simphony/cuds/meta. It is installed and invoked by the setup.py script.
