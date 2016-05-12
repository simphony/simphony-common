Engine Extensions
=================

Base class and tools for loading extension metadata into SimPhoNy.

For information on engine entry points, see :doc:`../extending_simphony`

.. rubric:: Classes

.. currentmodule:: simphony.engine

.. autosummary::
  :nosignatures:

   ~ABCEngineExtension
   ~EngineInterface
   ~extension.EngineMetadata
   ~extension.EngineFeatureMetadata
   ~extension.EngineManager
   ~exceptions.EngineManagerError

.. rubric:: Functions

.. autosummary::
   ~create_wrapper
   ~decorators.register
   ~get_supported_engine_names
   ~get_supported_engines

.. rubric:: Implementation

.. automodule:: simphony.engine
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: simphony.engine.extension
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: simphony.engine.exceptions
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: simphony.engine.decorators
    :members:
    :undoc-members:
    :show-inheritance: