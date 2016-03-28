""" Simphony engine module

This module is dynamicaly populated at import with the
registered plugins modules. Plugins modules need to be
registered at the 'simphony.engine' entry point.


"""

# A temporary solution to keep a list of wrappers known to SimPhoNy
_WRAPPER_REGISTRY = {}


def get_wrapper(wrapper_name):
    """Return corresponding wrapper class.

    Parameters
    ----------
    wrapper_name: str
        name that wrapper is registered with.
    """
    return _WRAPPER_REGISTRY.get(wrapper_name)


def get_wrappers():
    """Return a list of know wrappers."""
    return _WRAPPER_REGISTRY.keys()


def load_engine_extentions():
    """ Discover and load engine extension modules.

    """
    from stevedore import extension
    mgr = extension.ExtensionManager(
        namespace='simphony.engine',
        invoke_on_load=False)
    extensions = {}
    for extension in mgr.extensions:
        extensions[extension.name] = extension.plugin
        # Invoke 'get_wrappers' method and register wrappers.
        if hasattr(extension.plugin, 'get_wrappers'):
            wrappers = extension.plugin.get_wrappers()
            if wrappers:
                _WRAPPER_REGISTRY.update(wrappers)
    return extensions


# Populate the module namespace
globals().update(load_engine_extentions())

# cleanup
del load_engine_extentions
