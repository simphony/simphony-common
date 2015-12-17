Extending SimPhoNy
==================

Plugins
-------

The SimPhoNy library can extended through two `entry points`_ for
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


CUBA keywords
-------------

Common Unified Basic Attributes (CUBA) are a list of common keywords transcending
across different scales, methods and modelling-engines. As SimPhoNy is extended,
there is a need for CUBA to also be extended. Before adding a CUBA, developers
should first consult the list of existing :ref:`cuba-keywords`,
to see if the keyword already exists. Contact the developers at
https://github.com/simphony/simphony-common if there are any questions.

Once you have decided upon what CUBA needs to be added (or modified), edit
``simphony/core/cuba.yml`` to add the respective keyword. Ensure that all the
the required information is accurately provided.

Developers should then use cuba_generate.py to generate four files which are
based on the contents of cuba.yml::

   python simphony/scripts/cuba_generate.py python simphony/core/cuba.yml simphony/core/cuba.py
   python simphony/scripts/cuba_generate.py keywords simphony/core/cuba.yml simphony/core/keywords.py
   python simphony/scripts/cuba_generate.py rst simphony/core/cuba.yml doc/source/cuba.rst
   python simphony/scripts/cuba_generate.py table simphony/core/cuba.yml simphony/io/data_container_description.py

Finally, a pull request should be created and reviewed.

Also note that the H5_FILE_VERSION version of :class:`~.H5CUDS` will usually
have to be updated for each release of SimPhoNy when the list of CUBA keywords
has been modified.


Material Relationships
----------------------

Material relations are defined in ``simphony/core/material_relations.yml``.
Similar to extending CUBA, a script is used to generate multiple files based
on the content of 'material_relations.yml'::

   python simphony/scripts/material_relations_generate.py test simphony/core/material_relations.yml simphony/material_relations/tests/
   python simphony/scripts/material_relations_generate.py create_enum simphony/core/material_relations.yml simphony/core/cuds_material_relation.py
   python simphony/scripts/material_relations_generate.py python simphony/core/material_relations.yml simphony/material_relations/
   python  simphony/scripts/material_relations_generate.py material_relations_information simphony/core/material_relations.yml simphony/core/material_relations_information.py

A pull request should be created https://github.com/simphony/simphony-common
and reviewed by the SimPhoNy developers.

Note that the scripts create multiple files in ``simphony/material_relations/``.
Take care to ensure that any new files are included in your PR.  Also note that
the scripts will **only** create new files or update existing files in
``simphony/material_relations/``. So if you change the name of a material
relation, the still existing (but now outdated) file that has the old name
should be removed.
