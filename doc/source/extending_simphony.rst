Extending SimPhoNy
==================

Plugins
-------

The SimPhoNy library can be extended through two `entry points`_ for
contributing python modules that contain engine and visualisation components:

- ``simphony.engine`` -- A python module that provides one or more
  classes that implement the :class:`~.ABCModelingEngine` interface.

- ``simphony.visualisation`` -- A python module that provides a simple
  function to show (visualise the high-level CUDS containers)


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


Plugin metadata
---------------
Each plugin should implement a subclass of ``simphony.engine.extension.ABCEngineExtension`` and
put it inside its top-level package, i.e. the package that is registered at the entry point.

This a sample from simphony-lammps-md plugin::

    from simphony.engine import ABCEngineExtension
    from simphony.engine import EngineInterface

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
that the corresponing egnine provides in order to solve the physics equation. Features are
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
``simphony/core/cuba.yml`` to add the respective keyword. Ensure that all
the required information is accurately provided.

Developers should then use cuba_generate.py to generate four files which are
based on the contents of cuba.yml::

   python scripts/cuba_generate.py python simphony/core/cuba.yml simphony/core/cuba.py
   python scripts/cuba_generate.py keywords simphony/core/cuba.yml simphony/core/keywords.py
   python scripts/cuba_generate.py rst simphony/core/cuba.yml doc/source/cuba.rst
   python scripts/cuba_generate.py table simphony/core/cuba.yml simphony/io/data_container_description.py

Finally, a pull request should be created and reviewed.

Also note that the H5_FILE_VERSION version of :class:`~.H5CUDS` will usually
have to be updated for each release of SimPhoNy when the list of CUBA keywords
has been modified.


Material Relationships
----------------------

:ref:`Material relations <material-relations-table>` are defined in
``simphony/core/material_relation_definitions.yml``.
This information is used to generate different documentation and code.

Similar to extending CUBA, a script is used to generate multiple files
based on the content of ``material_relation_definitions.yml``::

   python scripts/material_relations_generate.py create_enum simphony/core/material_relation_definitions.yml simphony/core/cuds_material_relation.py
   python scripts/material_relations_generate.py python simphony/core/material_relation_definitions.yml simphony/cuds/material_relations/
   python scripts/material_relations_generate.py test simphony/core/material_relation_definitions.yml simphony/cuds/material_relations/tests/
   python scripts/material_relations_generate.py material_relations_definitions_py simphony/core/material_relation_definitions.yml simphony/core/material_relation_definitions.py
   python scripts/material_relations_generate.py table_rst simphony/core/material_relation_definitions.yml doc/source/material_relations_table.rst
   python scripts/material_relations_generate.py create_api simphony/core/material_relation_definitions.yml doc/source/api/material_relations.rst

A pull request should be created https://github.com/simphony/simphony-common
and reviewed by the SimPhoNy developers.

Note that the scripts create multiple files in ``simphony/material_relations/``.
Take care to ensure that any new files are included in your PR.  Also note that
the scripts will **only** create new files or update existing files in
``simphony/material_relations/``. So if you change the name of a material
relation, the still existing (but now outdated) file that has the old name
should be removed.
