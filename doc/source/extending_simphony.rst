Extending SimPhoNy
==================

Plugins
-------

The SimPhoNy library can extended through two `entry points`_ for
contributing python modules that contain engine and visualisation components:

- ``simphony.engine`` -- A python module that provides one or more
  classes that implement the :class:`ABCModelingEngine` interface.

- ``simphony.visualisation`` -- A python module that provides a simple
  function to show (visualise the high level CUDS containers)


To declare that a package contains a visualisation or engine module
for simphony, a developer has to add an entry point definition in the
``setup.py`` of the contributing package.

e.g.::

    setup(
       entry_points={
        'simphony.engine': ['<name> = <module_path>'])

Where ``<module_path>`` is a module where the engine class(es) can be
found like ``my_cool_engine_plugin.cool_engine342`` and ``<name>`` is
the user visible name that the ``cool_engine432`` module will have
inside the SimPhoNy framework. It is important that <name> is unique
and specific to the contributed components (e.g. name == 'default' is
probably a very bad choice)

e.g.::

    setup(
       entry_points={
        'simphony.engine': ['cool = my_cool_engine_plugin.cool_engine342'])

Will allow the user to import the new engine from inside the ``simphony`` module as follows

::

   from simphony.engine import cool
   # cool is now a reference to the external module ``my_cool_engine_plugin.cool_engine342``
   # If the name of the provided engine class is EngFast then the user should be able to do
   engine = cool.EngFast()


.. note::

   The ``examples/plugin`` folder of the simphony-common repository
   contains a dummy package that contributes python modules to both


.. _entry points : http://pythonhosted.org/setuptools/pkg_resources.html#entry-points


CUBA keywords
-------------

Common Unified Base Attributes (CUBA) are a list of common keywords transcending
across different scales, methods and modelling-engines. As SimPhoNy is extended,
there is a need for CUBA to also be extended. Before adding a CUBA, first
consult the list of existing CUBA keywords <cuba>, to see if the keyword already
exists. Contact the developers at https://github.com/simphony/simphony-common if
there are any questions.

Once you have decided upon the what CUBA needs to be added (or edited), edit
`simphony/core/cuba.yml` to add the respective keyword and the required
information.

Run cuba_generate.py to generate four files which are based on the contents of cuba.yml::

   python simphony/scripts/cuba_generate.py python simphony/core/cuba.yml simphony/core/cuba.py
   python simphony/scripts/cuba_generate.py keywords simphony/core/cuba.yml simphony/core/keywords.py
   python simphony/scripts/cuba_generate.py rst simphony/core/cuba.yml doc/source/cuba.rst
   python simphony/scripts/cuba_generate.py table simphony/core/cuba.yml simphony/io/data_container_description.py

Create a pull request with these changes and ask for a review.

Also note that the version of H5Cuds will have to also be incremented
