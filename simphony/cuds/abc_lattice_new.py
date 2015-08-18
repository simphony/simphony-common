from abc import ABCMeta, abstractmethod


class ABCLattice(object):
    """Abstract base class for a lattice.

    Attributes
    ----------
    name : str
        name of lattice
    size : int[3]
        lattice dimensions
    origin : float[3]
        lattice origin
    prim_cell : PrimitiveCell
        primitive cell specifying the 3D Bravais lattice
    data : DataContainer
        high level CUBA data assigned to lattice
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_node(self, index):  # pragma: no cover
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
    def update_nodes(self, nodes):  # pragma: no cover
        """Update the corresponding lattice nodes.

        Parameters
        ----------
        nodes : iterator of LatticeNodes

        """

    @abstractmethod
    def iter_nodes(self, indices=None):  # pragma: no cover
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
        p1 = self.prim_cell.p1
        p2 = self.prim_cell.p2
        p3 = self.prim_cell.p3
        return self.origin + index[0]*p1 + index[1]*p2 + index[2]*p3

    @abstractmethod
    def count_of(self, item_type):  # pragma: no cover
        """ Return the count of item_type in the container.

        Parameters
        ----------
        item_type : CUDSItem
            The CUDSItem enum of the type of the items to return the count of.

        Returns
        -------
        count : int
            The number of items of item_type in the container.

        Raises
        ------
        ValueError :
            If the type of the item is not supported in the current
            container.

        """
