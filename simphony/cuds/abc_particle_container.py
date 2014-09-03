"""
Interface for container that contains particles and bonds
"""
import abc


class ABCParticleContainer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def add_particle(p):
        """Add particle"""
        return

    @abc.abstractmethod
    def update_particle(p):
        """Update particle"""
        return

    @abc.abstractmethod
    def get_particle(id):
        """Get particle"""
        return

    @abc.abstractmethod
    def remove_particle(id):
        """Remove particle"""
        return

    @abc.abstractmethod
    def iter_particles(ids):
        """iter particles"""
        return

    @abc.abstractmethod
    def add_bond(b):
        """Add bond"""
        return

    @abc.abstractmethod
    def update_bond(b):
        """Update bond"""
        return

    @abc.abstractmethod
    def get_bond(id):
        """Get bond"""
        return

    @abc.abstractmethod
    def remove_bond(id):
        """Remove bond"""
        return

    @abc.abstractmethod
    def iter_bonds(ids):
        """iter bonds"""
        return
