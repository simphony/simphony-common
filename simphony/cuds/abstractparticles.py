# -*- coding: utf-8 -*-
from __future__ import print_function
from abc import ABCMeta, abstractmethod


class ABCParticleContainer(object):
    """Abstract base class for a ParticleContainer item.

    Attributes
    ----------
    name : str
        name of particle container
    """
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

    @abstractmethod
    def has_particle(self, id):
        pass

    @abstractmethod
    def has_bond(self, id):
        pass
