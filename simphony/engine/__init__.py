""" Simphony engine module

This module is dynamicaly populated at import with the
registered plugins modules. Plugins modules need to be
registered at the 'simphony.engine' entry point.
"""
from ..extension import get_engine_manager


__all__ = ['get_supported_engines',
           'get_supported_engine_names']


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
    engine_manager = get_engine_manager()
    for ext in mgr.extensions:
        extensions[ext.name] = ext.plugin
        # Load engine metadata
        engine_manager.load_metadata(ext.plugin)
    return extensions


# Populate the module namespace
globals().update(load_engine_extentions())

# cleanup
del load_engine_extentions
