"""
Interface for container that contains particles and bonds
"""
import abc


class ABCParticleContainer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def add_particle(p):
        """Add particle"""

    @abc.abstractmethod
    def update_particle(p):
        """Update particle"""

    @abc.abstractmethod
    def get_particle(id):
        """Get particle"""

    @abc.abstractmethod
    def remove_particle(id):
        """Remove particle"""

    @abc.abstractmethod
    def iter_particles(ids):
        """iter particles"""

    @abc.abstractmethod
    def add_bond(b):
        """Add bond"""

    @abc.abstractmethod
    def update_bond(b):
        """Update bond"""

    @abc.abstractmethod
    def get_bond(id):
        """Get bond"""

    @abc.abstractmethod
    def remove_bond(id):
        """Remove bond"""

    @abc.abstractmethod
    def iter_bonds(ids):
        """iter bonds"""
