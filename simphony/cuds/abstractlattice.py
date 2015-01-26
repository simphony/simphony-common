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
        """Get a copy of the node corresponding to the given index.

        Parameters:
        -----------
        index: tuple of D x int (node index coordinate)

        Returns:
        -----------
        A reference to a LatticeNode object
        """
        pass

    @abstractmethod
    def update_node(self, lat_node):
        """Update the corresponding lattice node (data copied).

        Parameters:
        -----------
        lat_node: reference to a LatticeNode object
            data copied from the given node
        """
        pass

    @abstractmethod
    def iter_nodes(self, indices=None):
        """Get an iterator over the LatticeNodes described by the indices.

        Parameters:
        -----------
        indices: iterable set of D x int (node index coordinates)

        Returns:
        -----------
        A generator for LatticeNode objects
        """
        pass

    @abstractmethod
    def get_coordinate(self, index):
        """Get coordinate of the given index coordinate.

        Parameters:
        -----------
        index: D x int (node index coordinate)

        Returns:
        -----------
        D x float
        """
        pass


def main():
    print("""Module for Lattice classes:
               ABCLattice ---> Common Base abstract class
               ("interface") for the Lattice.
          """)

if __name__ == '__main__':
    main()
