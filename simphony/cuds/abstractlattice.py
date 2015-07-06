from abc import ABCMeta, abstractmethod


class ABCLattice(object):
    """Abstract base class for a lattice.

    Attributes
    ----------
    name : str
        name of lattice
    type : str
        type of lattice
    base_vect : float[3]
        base vector of lattice
    size : int[3]
        lattice dimensions
    origin : float[3]
        lattice origin
    data : DataContainer
        high level CUBA data assigned to lattice

    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_node(self, index):
        """Get the lattice node corresponding to the given index.

        Parameters
        ----------
        index : int[3]
            node index coordinate

        Returns
        -------
        node : LatticeNode

        """

    @abstractmethod
    def update_node(self, node):
        """Update the corresponding lattice node.

        Parameters
        ----------
        node : LatticeNode

        """

    @abstractmethod
    def iter_nodes(self, indices=None):
        """Get an iterator over the LatticeNodes described by the indices.

        Parameters
        ----------
        indices : iterable set of int[3], optional
            When indices (i.e. node index coordinates) are provided, then nodes
            are returned in the same order of the provided indices. If indices
            is None, there is no restriction on the order the nodes that are
            returned.

        Returns
        -------
        iterator:
            An iterator over LatticeNode objects

        """

    @abstractmethod
    def get_coordinate(self, index):
        """Get coordinate of the given index coordinate.

        Parameters
        ----------
        index : int[3]
            node index coordinate

        Returns
        -------
        coordinates : float[3]

        """

    @abstractmethod
    def count_of(self, item_type):
        pass
