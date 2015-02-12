from abc import ABCMeta, abstractmethod


class ABCLattice(object):
    """Abstract base class for a lattice.

    Attributes
    ----------
    name : str
        name of lattice
    type : str
        type of lattice
    base_vect : tuple of D x float
        base vector of lattice
    size : tuple of D x int
        lattice dimensions
    origin : tuple of D x float
        lattice origin

    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_node(self, index):
        """Get the lattice node corresponding to the given index.

        Parameters:
        -----------
        index: tuple of D x int
            node index coordinate

        Returns:
        --------
        LatticeNode

        """
        pass

    @abstractmethod
    def update_node(self, lat_node):
        """Update the corresponding lattice node.

        Parameters:
        -----------
        lat_node: LatticeNode

        """
        pass

    @abstractmethod
    def iter_nodes(self, indices=None):
        """Get an iterator over the LatticeNodes described by the indices.

        Parameters:
        -----------
        indices: iterable set of D x int, optional
            node index coordinates
        Returns:
        --------
        A generator for LatticeNode objects

        """
        pass

    @abstractmethod
    def get_coordinate(self, index):
        """Get coordinate of the given index coordinate.

        Parameters:
        -----------
        index: D x int
            node index coordinate

        Returns:
        --------
        D x float

        """
        pass
