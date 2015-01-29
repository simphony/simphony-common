""" Simphony engine module

This module is dynamicaly populated at import with the
registered plugins modules. Plugins modules need to be
registered at the 'simphony.engine' entry point.


"""


def load_engine_extentions():
    """ Discover and load engine extension modules.

    """
    from stevedore import extension
    mgr = extension.ExtensionManager(
        namespace='simphony.engine',
        invoke_on_load=False)
    return {extension.name: extension.plugin for extension in mgr.extensions}


# Populate the module namespace
globals().update(load_engine_extentions())

# cleanup
del load_engine_extentions
