"""Contains simulation controllers."""
from . import CUDS
from ..engine import get_wrapper


class WrapperFactory(object):
    """Creates wrappers."""
    @staticmethod
    def create(wrapper_name, cuds):
        """Create a wrapper instance of the given name.

        Parameters
        ----------
        cuds: CUDS
            a cuds object containing simulation data
        wrapper_name: str
            A SimPhoNy wrapper name, should be of of registered engines.
        """
        wrapper = get_wrapper(wrapper_name)
        if not wrapper:
            raise Exception('Unknown wrapper: %s' % wrapper_name)

        return wrapper(cuds=cuds)


class Simulation(object):
    """Represents a simulation using CUDS.

    Parameters
    ----------
    cuds: CUDS
        A cuds object which contains model information.
    wrapper_name: str
        Name of the wrapper to launch the simulation with.
    """
    def __init__(self, cuds, wrapper_name):
        self._cuds = cuds
        self._wrapper = WrapperFactory.create(wrapper_name, cuds)

    def run(self, *args, **kwargs):
        """Run the simulation."""
        self._wrapper.run(*args, **kwargs)
