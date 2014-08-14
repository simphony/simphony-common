# -*- coding: utf-8 -*-
"""
    Module for Abstract Particle class:
        ABCParticlesContainer ---> Common Base abstract class ("interface") for
            the the Particles container.
"""

from abc import ABCMeta, abstractmethod
import random
from sys import maxint


class ABCParticlesContainer(object):
    """Abstract base class for a ParticleContainer item."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_particle(self, new_particle):
        pass

    @abstractmethod
    def add_bond(self, new_bond):
        pass

    @abstractmethod
    def update_particle(self, particle):
        pass

    @abstractmethod
    def update_bond(self, bond):
        pass

    @abstractmethod
    def get_particle(self, particle_id):
        pass

    @abstractmethod
    def get_bond(self, bond_id):
        pass

    @abstractmethod
    def remove_particle(self, particle_id):
        pass

    @abstractmethod
    def remove_bond(self, bond_id):
        pass

    @abstractmethod
    def iter_particles(self, particle_ids=None):
        pass

    @abstractmethod
    def iter_bonds(self, bond_ids=None):
        pass


class ElementsCommon(object):
    """Base Class that overrides standard methods for comparison and string
    conversion (in case we need it).

    Also has some common attributes for derived classes (Particles and Bonds
    for the moment).

    Attributes
    ----------
        _id : int (for the moment)
            unique id of the element
        data : DataContainer
            data attributes of the element (not implemented yet)
    """
    def __init__(self, external_id=0):
        """open question: how should we manage the id? since add_particle method
        of ParticlesContainer gets a Particle as parameter, the id should be
        created automatically here inside Particle when we create a new one?
        In the case is automatically generated: should it be private so the
        user can't change it?. - Same for Bonds.
        """
        if external_id == 0:
            # stub --> generate random
            self._id = random.randint(-maxint, maxint)
        else:
            self._id = external_id

        # when ready:
        # self.data = DataContainer()

    def get_id(self):
        return self._id

    def __lt__(self, other):
        return self._id < other.get_id()

    def __le__(self, other):
        return self._id <= other.get_id()

    def __eq__(self, other):
        return self._id == other.get_id()

    def __ne__(self, other):
        return self._id != other.get_id()

    def __gt__(self, other):
        return self._id > other.get_id()

    def __ge__(self, other):
        return self._id >= other.get_id()

    def __str__(self):
        pass

    def __repr__(self):
        # text = "%d_%lf_%lf_%lf" % self.__id, self.x, self.y, self.z
        return self.__str__()


# Just an information message of the module
def main():
    print """Module for Particle classes:
               ABCParticlesContainer ---> Common Base abstract class
               ("interface") for the the Particles container.
           """

if __name__ == '__main__':
    main()
