# -*- coding: utf-8 -*-
from __future__ import print_function
from abc import ABCMeta, abstractmethod


class ABCParticles(object):
    """Abstract base class for a Particles item.

    Attributes
    ----------
    name : str
        name of particles item.
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
    def get_particle(self, uid):
        pass

    @abstractmethod
    def get_bond(self, uid):
        pass

    @abstractmethod
    def remove_particle(self, uid):
        pass

    @abstractmethod
    def remove_bond(self, uid):
        pass

    @abstractmethod
    def iter_particles(self, uids=None):
        pass

    @abstractmethod
    def iter_bonds(self, uids=None):
        pass

    @abstractmethod
    def has_particle(self, uid):
        pass

    @abstractmethod
    def has_bond(self, uid):
        pass
