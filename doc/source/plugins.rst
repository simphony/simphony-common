Plugins
=======

The SimPhoNy library can extended through two `entry points`_ for
contributing python modules that container engine and visualization components:

- ``simphony.engine`` -- A python module that provides one or more
  classes that implement the :class:`ABCModelingEngine` interface.

- ``simphony.visualization`` -- A python module that provides a simple
  function to show (visualise the high level CUDS containers)


To declare that a package contains a visualization or engine modules
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
