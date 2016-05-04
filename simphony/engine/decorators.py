"""Engine related decorators."""
from . import get_engine_manager


def register(cls):
    """Register an engine extension metadata.

    Parameters
    ----------
    cls: ABCEngineExtension
      a subclass of base extension metadata type
    """
    # Register the given class on the current engine manager.
    get_engine_manager().register(cls)
    return cls
