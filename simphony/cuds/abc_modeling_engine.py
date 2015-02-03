from abc import ABCMeta, abstractmethod


class ABCModelingEngine(object):
    """Abstract base class for a modeling engines in SimPhoNy

    Attributes
    ----------
    BC : DataContainer
        container of attributes related to the bondary conditions
    CM : DataContainer
        container of attributes related to the computational method
    SP : DataContainer
        container of attributes related to the system paremters/conditions

    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def add_lattice(self, name, lattice):
        pass

    @abstractmethod
    def add_mesh(self, name, mesh):
        pass

    @abstractmethod
    def add_particle_container(self, name, pc):
        pass

    @abstractmethod
    def delete_lattice(self, name):
        pass

    @abstractmethod
    def delete_mesh(self, name):
        pass

    @abstractmethod
    def delete_particle_container(self, name):
        pass

    @abstractmethod
    def get_lattice(self, name):
        pass

    @abstractmethod
    def get_mesh(self, name):
        pass

    @abstractmethod
    def get_particle_container(self, name):
        pass

    @abstractmethod
    def iter_lattices(self, names=None):
        pass

    @abstractmethod
    def iter_mesh(self, names=None):
        pass

    @abstractmethod
    def iter_particle_container(self, names=None):
        pass
