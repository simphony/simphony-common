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
    """Return a list of known wrappers."""
    return _WRAPPER_REGISTRY.keys()


def _update_wrappers(wrappers):
    """Update the wrapper registry.

    Parameters
    ----------
    wrappers: dict
        key/ABCModelingEngine class pairs
    """
    if not wrappers:
        return

    if not isinstance(wrappers, dict):
        raise TypeError('Must be a dict of key/ABCModelingEngine pairs.')

    for key in wrappers.keys():
        if key in _WRAPPER_REGISTRY:
            raise ValueError('A wrapper already exists for the key %s' % key)
    _WRAPPER_REGISTRY.update(wrappers)


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
        # Invoke 'get_wrappers' method and register wrappers.
        if hasattr(ext.plugin, 'get_wrappers') and \
                callable(ext.plugin.get_wrappers):
            _update_wrappers(ext.plugin.get_wrappers())
    return extensions


# Populate the module namespace
globals().update(load_engine_extentions())

# cleanup
del load_engine_extentions
