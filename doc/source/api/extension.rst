Engine Extensions
=================

Base class and tools for loading extension metadata into SimPhoNy.

For information on engine entry points, see :doc:`../extending_simphony`

.. rubric:: Classes

.. currentmodule:: simphony.extension

.. autosummary::
  :nosignatures:

   ~extension.ABCEngineExtension
   ~extension.EngineInterface
   ~extension.EngineMetadata
   ~extension.EngineFeatureMetadata
   ~extension.EngineManagerException
   ~extension.EngineManager

.. rubric:: Functions

.. autosummary::
   ~get_engine_manager
   ~create_wrapper

.. currentmodule:: simphony.engine
.. autosummary::
   ~get_supported_engine_names
   ~get_supported_engines

.. rubric:: Implementation

.. automodule:: simphony.extension
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: simphony.extension.extension
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: simphony.engine
    :members:
    :undoc-members:
    :show-inheritance:
