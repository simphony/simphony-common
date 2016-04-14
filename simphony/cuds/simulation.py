"""Contains simulation controllers."""
from . import CUDS
from ..engine import create_wrapper


class Simulation(object):
    """A CUDS computational model simulation.

    Parameters
    ----------
    cuds: CUDS
        A cuds object which contains model information.
    engine_name: str
        Name of the underlying engine to launch the simulation with.
    engine_interface: EngineInterface
        The interface to the engine, internal or fileio.
    """
    def __init__(self, cuds, engine_name, engine_interface=None):
        if not isinstance(cuds, CUDS):
            raise TypeError('Expected CUDS but got %s' % type(cuds))
        self._cuds = cuds
        self._wrapper = create_wrapper(cuds,
                                       engine_name,
                                       engine_interface=engine_interface)

    def run(self, *args, **kwargs):
        """Run the simulation."""
        self._wrapper.run(*args, **kwargs)
