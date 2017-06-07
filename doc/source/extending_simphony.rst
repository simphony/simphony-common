Extending SimPhoNy
==================

Plugins
-------

The SimPhoNy library can be extended through three `entry points`_ for
contributing python modules that contain engine, visualisation and
pre-processing components:

- ``simphony.engine`` -- A python module that provides one or more
  classes that implement the :class:`~.ABCModelingEngine` interface.

- ``simphony.visualisation`` -- A python module that provides a simple
  function to show (visualise the high-level CUDS containers)

- ``simphony.pre_processing`` -- A python module that provides
  pre-processing tools and utilities


To declare that a package contains a visualisation, engine or pre_processing 
module for simphony, a developer has to add an entry point definition in the
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


Plugin metadata
---------------
Each plugin should implement a subclass of ``ABCEngineExtension`` and
put it inside its top-level package, i.e. the package that is registered at the entry point.
Moreover, this class should be registered using ``register`` decorator. The class's ``__name__``
attribute will be used as its identifier.

This a sample from simphony-lammps-md plugin::

    from simphony.engine import ABCEngineExtension
    from simphony.engine import EngineInterface
    from simphony.engine.decorators import register


    @register
    class SimlammpsExtension(ABCEngineExtension):
        def get_supported_engines(self):
            lammps_features =\
                self.create_engine_metadata_feature(MolecularDynamics(),
                                                    [Verlet()])
            liggghts_features =\
                self.create_engine_metadata_feature(GranularDynamics(),
                                                    [DEM()])
            lammps = self.create_engine_metadata('LAMMPS',
                                                 lammps_features,
                                                 [EngineInterface.Internal,
                                                  EngineInterface.FileIO])
            liggghts = self.create_engine_metadata('LIGGGHTS',
                                                   liggghts_features,
                                                   [EngineInterface.FileIO])
            return [lammps, liggghts]

        def create_wrapper(self, cuds, engine_name, engine_interface):
            use_internal_interface = False
            if engine_interface == EngineInterface.Internal:
                use_internal_interface = True
            if engine_name == 'LAMMPS':
                return LammpsWrapper(cuds=cuds,
                                     engine_type=EngineType.MD,
                                     use_internal_interface=use_internal_interface)
            elif engine_name == 'LIGGGHTS':
                return LammpsWrapper(cuds=cuds,
                                     engine_type=EngineType.DEM,
                                     use_internal_interface=use_internal_interface)
            else:
                raise Exception('Only LAMMPS and LIGGGHTS engines are supported. '
                                'Unsupported eninge: %s', engine_name)


SimPhoNy will inspect the plugins for subclasses of ``ABCEngineExtension``. SimPhoNy
creates an instance of each class and keeps track of available wrappers and their capabilities.
As implemented in the above example, there are two methods that should be implemented by
wrapper developers. ``create_wrapper`` is a factory method that receives a ``CUDS``, an
engine name and an interface (according to ``EngineInterface`` enum). This method must
create a wrapper instance and return it.

The other method is ``get_supported_engines``. This method must create and return a list of
the engine's features. Features are simply a pair of physics equation and a list of methods
that the corresponing engine provides in order to solve the physics equation. Features are
created by calling the ``create_engine_metadata_feature``. After creating features one must
pass them to the ``create_engine_metadata`` method in order to create metadata objects. Each
engine metadata object is a pair of engine name and a list of features provided by that engine.

Having this class implemented in the wrapper plugin, one can query for the available engines::

    >>> from simphony.engine import get_supported_engine_names
    >>> get_supported_engine_names()
    ['LIGGGHTS', 'LAMMPS']

CUBA keywords
-------------

Common Unified Basic Attributes (CUBA) are a list of common keywords transcending
across different scales, methods and modelling-engines. As SimPhoNy is extended,
there is a need for CUBA to also be extended. Before adding a CUBA, developers
should first consult the list of existing :ref:`cuba-keywords`,
to see if the keyword already exists. Contact the developers at
https://github.com/simphony/simphony-common if there are any questions.

Once you have decided upon what CUBA needs to be added (or modified), edit
``ontology/cuba.yml`` or ``ontology/simphony_metadata.yml`` to add the 
respective keyword. Ensure that all the required information is accurately 
provided.

The build process triggered by the setup.py will autogenerate files which are
based on the contents of the yml files. 

Finally, a pull request should be created and reviewed.

Also note that the H5_FILE_VERSION version of :class:`~.H5CUDS` will usually
have to be updated for each release of SimPhoNy when the list of CUBA keywords
has been modified.

