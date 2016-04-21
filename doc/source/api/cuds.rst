CUDS
====

Abstract CUDS interfaces
------------------------

.. rubric:: Engine and Containers

.. currentmodule:: simphony.cuds

.. autosummary::

   ~abc_modeling_engine.ABCModelingEngine
   ~abc_mesh.ABCMesh
   ~abc_particles.ABCParticles
   ~abc_lattice.ABCLattice


.. rubric:: Description

.. automodule:: simphony.cuds.abc_mesh
   :members:
   :undoc-members:

.. automodule:: simphony.cuds.abc_particles
   :members:
   :undoc-members:

.. automodule:: simphony.cuds.abc_lattice
   :members:
   :undoc-members:

.. automodule:: simphony.cuds.abc_modeling_engine
   :members:
   :undoc-members:

CUDS Computational Model
------------------------
.. rubric:: Container and Simulation

.. currentmodule:: simphony.cuds

.. autosummary::

   ~model.CUDS
   ~simulation.Simulation

.. rubric:: Description

.. automodule:: simphony.cuds.model
   :members:
   :undoc-members:

.. automodule:: simphony.cuds.simulation
   :members:
   :undoc-members:

Pure Python implementation
--------------------------

.. rubric:: Classes

.. currentmodule:: simphony.cuds

.. autosummary::

   ~primitive_cell.PrimitiveCell
   ~primitive_cell.BravaisLattice
   ~lattice.Lattice
   ~lattice.LatticeNode
   ~particles.Particles
   ~particles.Bond
   ~particles.Particle
   ~mesh.Mesh
   ~mesh.Point
   ~mesh.Edge
   ~mesh.Face
   ~mesh.Cell
   ~material.Material
   ~materials.Materials
   ~material_relations.material_relation.MaterialRelation


.. rubric:: Functions

.. autosummary::

   ~lattice.make_cubic_lattice
   ~lattice.make_body_centered_cubic_lattice
   ~lattice.make_face_centered_cubic_lattice
   ~lattice.make_rhombohedral_lattice
   ~lattice.make_tetragonal_lattice
   ~lattice.make_body_centered_tetragonal_lattice
   ~lattice.make_hexagonal_lattice
   ~lattice.make_orthorhombic_lattice
   ~lattice.make_body_centered_orthorhombic_lattice
   ~lattice.make_face_centered_orthorhombic_lattice
   ~lattice.make_base_centered_orthorhombic_lattice
   ~lattice.make_monoclinic_lattice
   ~lattice.make_base_centered_monoclinic_lattice
   ~lattice.make_triclinic_lattice

.. rubric:: Implementation

.. automodule:: simphony.cuds.lattice
   :members:
   :undoc-members:

.. automodule:: simphony.cuds.mesh
   :members:
   :undoc-members:

.. automodule:: simphony.cuds.particles
   :members:
   :undoc-members:

.. automodule:: simphony.cuds.material
   :members:
   :undoc-members:

.. automodule:: simphony.cuds.materials
   :members:
   :undoc-members:

.. automodule:: simphony.cuds.material_relations.material_relation
   :members:
   :undoc-members:

Material relations
------------------
For each ``kind`` of material relation, there exists a
subclass of :class:`~.MaterialRelation`.  See
:ref:`list of material relations <material-relations-table>` for more details.


.. include:: material_relations.rst

