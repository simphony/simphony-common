from abc import ABCMeta, abstractmethod


class ABCModelingEngine(object):
    """Abstract base class for modeling engines in SimPhoNy.

    Through this interface, the user controls and interacts with the
    simulation/calculation (which is being performed by the modeling
    engine).

    Attributes
    ----------
    BC : DataContainer
        container of attributes related to the boundary conditions
    CM : DataContainer
        container of attributes related to the computational method
    SP : DataContainer
        container of attributes related to the system parameters/conditions

    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):  # pragma: no cover
        """ Run the modeling engine

        Run the modeling engine using the configured settings (e.g. CM, BC,
        and SP) and the configured state data (e.g. particle, mesh and
        lattice data).
        """

    @abstractmethod
    def add_dataset(self, container):  # pragma: no cover
        """Add a CUDS container

        Parameters
        ----------
        container : {ABCMesh, ABCParticles, ABCLattice}
            The CUDS container to add to the engine.

        Raises
        ------
        TypeError:
            If the container type is not supported by the engine.
        ValueError:
            If there is already a dataset with the given name.

        """

    @abstractmethod
    def remove_dataset(self, name):  # pragma: no cover
        """ Remove a dataset from the internal

        Parameters
        ----------
        name: str
            name of CUDS container to be deleted

        Raises
        ------
        ValueError:
            If there is no dataset with the given name

        """

    @abstractmethod
    def get_dataset(self, name):  # pragma: no cover
        """ Get the dataset

        Parameters
        ----------
        name: str
            name of CUDS container to be retrieved.

        Returns
        -------
        container :
            A proxy of the dataset named ``name`` that is stored
            internally in the Engine.

        Raises
        ------
        ValueError:
            If there is no dataset with the given name

        """

    @abstractmethod
    def iter_datasets(self, names=None):  # pragma: no cover
        """ Returns an iterator over a subset or all of the containers.

        Parameters
        ----------
        names : sequence of str, optional
            names of specific containers to be iterated over. If names is not
            given, then all containers will be iterated over.

        """
