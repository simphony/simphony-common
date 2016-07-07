""" Simphony visualisation module

This module is dynamicaly populated at import with the
registered plugins modules. Plugins modules need to be
registered at the 'simphony.visualisation' entry point.


"""


def load_visualisation_extentions():
    """ Discover and load visualisation extension modules.

    """
    print "--- load_visualisation_extentions ---"
    from stevedore import extension
    mgr = extension.ExtensionManager(
        namespace='simphony.visualisation',
        invoke_on_load=False)
    return {extension.name: extension.plugin for extension in mgr.extensions}


# Populate the module namespace
globals().update(load_visualisation_extentions())

# cleanup
del load_visualisation_extentions
