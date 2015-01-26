# -*- coding: utf-8 -*-
"""
    Module for Abstract Lattice class:
        ABCLattice ---> Common Base abstract class ("interface") for
            the Lattice.
"""

from __future__ import print_function
from abc import ABCMeta, abstractmethod


class ABCLattice(object):
    """Abstract base class for a Lattice item."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_node(self, index):
        pass

    @abstractmethod
    def update_node(self, lat_node):
        pass

    @abstractmethod
    def iter_nodes(self, indices=None):
        pass

    @abstractmethod
    def get_coordinate(self, index):
        pass


def main():
    print("""Module for Lattice classes:
               ABCLattice ---> Common Base abstract class
               ("interface") for the Lattice.
          """)

if __name__ == '__main__':
    main()
