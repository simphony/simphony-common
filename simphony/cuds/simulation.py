"""Contains simulation controllers."""
from . import CUDS
from ..engine import create_wrapper


class Simulation(object):
    """A CUDS computational model simulation.

    Parameters
    ----------
    cuds: CUDS
        Model information.
    engine_name: str
        Name of the underlying engine.
    engine_interface: engine.EngineInterface
        The interface to the engine, internal or fileio.
    name: str
        A custom name for this simulation
    description: str
        More information about this simulation
    """
    def __init__(self, cuds, engine_name, engine_interface=None,
                 name=None,
                 description=None):
        self.name = name
        self.description = description

        if not isinstance(cuds, CUDS):
            raise TypeError('Expected CUDS but got %s' % type(cuds))
        self._cuds = cuds
        self._wrapper = create_wrapper(cuds,
                                       engine_name,
                                       engine_interface=engine_interface)

    def run(self, *args, **kwargs):
        """Run the simulation."""
        self._wrapper.run(*args, **kwargs)

    def get_cuds(self):
        """Return the latest CUDS from the engine.

        Returns
        -------
        cuds: CUDS
            the most recent CUDS.
        """
        return self._wrapper.get_cuds()
