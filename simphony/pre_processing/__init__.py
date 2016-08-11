""" Simphony pre_processing module

This module is dynamicaly populated at import with the
registered plugins modules. Plugins modules need to be
registered at the 'simphony.pre_processing' entry point.


"""


def load_pre_processing_extentions():
    """ Discover and load pre_processing extension modules.

    """
    from stevedore import extension
    mgr = extension.ExtensionManager(
        namespace='simphony.pre_processing',
        invoke_on_load=False)
    extensions = {}
    for ext in mgr.extensions:
        extensions[ext.name] = ext.plugin
    return extensions


# Populate the module namespace
globals().update(load_pre_processing_extentions())

# cleanup
del load_pre_processing_extentions
