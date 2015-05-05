CUDS
====


Abstract CUDS interfaces
------------------------

.. rubric:: Containers

.. currentmodule:: simphony.cuds

.. autosummary::

   ~abstractmesh.ABCMesh
   ~abstractparticles.ABCParticles
   ~abstractlattice.ABCLattice

.. rubric:: Description

.. automodule:: simphony.cuds.abstractmesh
   :members:
   :undoc-members:

.. automodule:: simphony.cuds.abstractparticles
   :members:
   :undoc-members:

.. automodule:: simphony.cuds.abstractlattice
   :members:
   :undoc-members:

Pure Python implementation
--------------------------

.. rubric:: Classes

.. currentmodule:: simphony.cuds

.. autosummary::

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

.. rubric:: Functions

.. autosummary::

   ~lattice.make_hexagonal_lattice
   ~lattice.make_square_lattice
   ~lattice.make_rectangular_lattice
   ~lattice.make_cubic_lattice
   ~lattice.make_orthorombicp_lattice

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
