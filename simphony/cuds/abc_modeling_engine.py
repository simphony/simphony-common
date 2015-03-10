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
    def run(self):
        """Run the modeling engine

        Run the modeling engine using the configured settings (e.g. CM, BC,
        and SP) and the configured state data (e.g. particle, mesh and
        lattice data).

        """
        pass

    @abstractmethod
    def add_lattice(self, lattice):
        """Add lattice to the modeling engine

        Parameters
        ----------
        lattice : ABCLattice
            lattice to be added.

        Returns
        -------
        proxy : ABCLattice
            A lattice to be used to update/query the internal representation
            stored inside the modeling-engine. See get_lattice for more
            information.

        """
        pass

    @abstractmethod
    def add_mesh(self, mesh):
        """Add mesh to the modeling engine

        Parameters
        ----------
        mesh: ABCMesh
            mesh to be added.

        Returns
        -------
        proxy : ABCMesh
            A proxy mesh to be used to update/query the internal representation
            stored inside the modeling-engine. See get_mesh for more
            information.
        """
        pass

    @abstractmethod
    def add_particles(self, particles):
        """Add particle container to the modeling engine

        Parameters
        ----------
        particles: ABCParticles
            particle container to be added.

        Returns
        -------
        ABCParticles
            A particle container to be used to update/query the internal
            representation stored inside the modeling-engine. See
            get_particles for more information.

        """
        pass

    @abstractmethod
    def delete_lattice(self, name):
        """Delete a lattice

        Parameters
        ----------
        name: str
            name of lattice to be deleted

        """
        pass

    @abstractmethod
    def delete_mesh(self, name):
        """Delete a mesh

        Parameters
        ----------
        name: str
            name of mesh to be deleted

        """
        pass

    @abstractmethod
    def delete_particles(self, name):
        """Delete a particle container

        Parameters
        ----------
        name: str
            name of particle container to be deleted

        """
        pass

    @abstractmethod
    def get_lattice(self, name):
        """ Get lattice

        The returned lattice can be used to query and update the state of the
        lattice inside the modeling engine.

        Returns
        -------
        ABCLattice

        """
        pass

    @abstractmethod
    def get_mesh(self, name):
        """ Get mesh

        The returned mesh can be used to query and update the state of the
        mesh inside the modeling engine.

        Returns
        -------
        ABCMesh

        """
        pass

    @abstractmethod
    def get_particles(self, name):
        """ Get particle container

        The returned particle container can be used to query and update the
        state of the particle container inside the modeling engine.

        Returns
        -------
        ABCParticles

        """
        pass

    @abstractmethod
    def iter_lattices(self, names=None):
        """ Returns an iterator over a subset or all of the lattices.

        Parameters
        ----------
        names : sequence of str, optional
            names of specific lattices to be iterated over. If names is not
            given, then all lattices will be iterated over.

        """
        pass

    @abstractmethod
    def iter_meshes(self, names=None):
        """ Returns an iterator over a subset or all of the meshes.

        Parameters
        ----------
        names : sequence of str, optional
            names of specific meshes to be iterated over. If names is not
            given, then all meshes will be iterated over.

        """
        pass

    @abstractmethod
    def iter_particles(self, names=None):
        """ Returns an iterator over a subset or all of the particle containers.

        Parameters
        ----------
        names : sequence of str, optional
            names of specific particle containers to be iterated over.
            If names is not given, then all particle containers will
            be iterated over.

        """
        pass
