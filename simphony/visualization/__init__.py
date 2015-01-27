""" Simphony visualization module

This module is dynamicaly populated at import with the
registered plugins modules. Plugins modules need to be
registered at the 'simphony.visualization' entry point.


"""


def load_visualization_extentions():
    """ Discover and load visualization extension modules.

    """
    from stevedore import extension
    mgr = extension.ExtensionManager(
        namespace='simphony.visualisation',
        invoke_on_load=False)
    return {extension.name: extension.plugin for extension in mgr.extensions}


# Populate the module namespace
globals().update(load_visualization_extentions())

# cleanup
del load_visualization_extentions
