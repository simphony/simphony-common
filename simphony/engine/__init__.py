""" Simphony engine module

This module is dynamicaly populated at import with the
registered plugins modules. Plugins modules need to be
registered at the 'simphony.engine' entry point.
"""
from .extension import ABCEngineExtension
from .extension import EngineInterface
from .extension import EngineManager


__all__ = ['ABCEngineExtension', 'EngineInterface',
           'get_supported_engines', 'create_wrapper',
           'get_supported_engine_names']


# TODO: Use an application server and put this in app context.
# Wrapper manager class.
_ENGINE_MANAGER = EngineManager()


def get_supported_engine_names():
    """Show a list of supported engine names.

    Returns
    -------
    names: list
        a list of engine names.
    """
    return _ENGINE_MANAGER.get_supported_engine_names()


def get_supported_engines():
    """Show a list of supported engines.

    Returns
    -------
    metadata: list
        a list of engine metadata objects
    """
    return _ENGINE_MANAGER.get_supported_engines()


def create_wrapper(cuds, engine_name, engine_interface=None):
    """Create a wrapper to the given engine.

    Parameters
    ----------
    cuds: CUDS
        A cuds object which contains model information.
    engine_name: str
        Name of the underlying engine to launch the simulation with.
    engine_interface: engine.EngineInterface
        The interface to the engine, internal or fileio.

    Returns
    -------
    wrapper: engine.ABCEngineExtension
        an engine wrapper instance
    """
    return _ENGINE_MANAGER.create_wrapper(cuds, engine_name, engine_interface)


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
        # Load engine metadata
        _ENGINE_MANAGER.load_metadata(ext.plugin)
    return extensions


# Populate the module namespace
globals().update(load_engine_extentions())

# cleanup
del load_engine_extentions
