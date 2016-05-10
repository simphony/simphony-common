""" Simphony engine module

This module is dynamically populated at import with the
registered plugins modules. Plugins modules need to be
registered at the 'simphony.engine' entry point.
"""
from .extension import ABCEngineExtension
from .extension import EngineInterface
from .extension import EngineManager

__all__ = ['create_wrapper',
           'get_supported_engines',
           'get_supported_engine_names',
           'ABCEngineExtension', 'EngineInterface']


# TODO: Use an application server and put this in app context.
# Wrapper manager class.
_ENGINE_MANAGER = EngineManager()


def get_engine_manager():
    """Get the engine manager instance."""
    return _ENGINE_MANAGER


def create_wrapper(cuds, engine_name, engine_interface=None):
    """Create a wrapper to the given engine.

    Parameters
    ----------
    cuds: CUDS
        a cuds object which contains model information
    engine_name: str
        name of the underlying engine to launch the simulation with
    engine_interface: engine.EngineInterface
        the interface to the engine, internal or fileio

    Returns
    -------
    wrapper: engine.ABCEngineExtension
        an engine wrapper instance
    """
    return get_engine_manager().create_wrapper(cuds,
                                               engine_name,
                                               engine_interface)


def get_supported_engine_names():
    """Show a list of supported engine names.

    Returns
    -------
    names: list
        a list of engine names
    """
    return get_engine_manager().get_supported_engine_names()


def get_supported_engines():
    """Show a list of supported engines.

    Returns
    -------
    metadata: list
        a list of engine metadata objects
    """
    return get_engine_manager().get_supported_engines()


def load_engine_extentions():
    """ Discover and load engine extension modules.

    """
    from stevedore import extension
    mgr = extension.ExtensionManager(
        namespace='simphony.engine',
        invoke_on_load=False)
    extensions = {}
    for ext in mgr.extensions:
        extensions[ext.name] = ext.plugin
    return extensions


# Populate the module namespace
globals().update(load_engine_extentions())

# cleanup
del load_engine_extentions
