from abc import abstractmethod

from ..core.cuds_item import CUDSItem
from .abc_dataset import ABCDataset
from .utils import deprecated


class ABCLattice(ABCDataset):
    """Abstract base class for a lattice.

    Attributes
    ----------
    name : str
        name of lattice
    primitive_cell : PrimitiveCell
        primitive cell specifying the 3D Bravais lattice
    size : int[3]
        lattice dimensions
    origin : float[3]
        lattice origin
    data : DataContainer
        high level CUBA data assigned to lattice
    """

    def get(self, index):
        """Returns a copy of the node with the given index

        Parameters
        ----------

        index : int[3]
            node index coordinate

        Raises
        ------
        KeyError :
            when the node is not in the container.

        Returns
        -------
        object :
            A copy of the internally stored info.
        """
        return self._get_node(index)

    def add(self, iterable):
        """Adds a set of objects from the provided iterable
        to the dataset.

        Currently not implemented.
        """
        raise NotImplementedError()

    def update(self, iterable):
        """Updates a set of nodes from the provided iterable.

        Takes the indexes of the nodes and searches inside the dataset for
        those nodes objects. If the node exists, they are replaced in the
        dataset. If any node doesn't exist, it will raise an exception.

        Parameters
        ----------

        iterable : iterable of nodes
            the nodes that will be replaced.

        Raises
        ------
        ValueError :
            If any node inside the iterable does not exist.
        """
        self._update_nodes(iterable)

    def remove(self, index):
        """Removes a set of nodes with the provided indexes
        from the dataset.

        Currently not implemented.
        """
        raise NotImplementedError()

    def iter(self, indices=None, item_type=None):
        """Generator method for iterating over the objects of the container.

        It can receive any kind of sequence of indices to iterate over
        those concrete objects. If nothing is passed as parameter, it will
        iterate over all the objects.

        Parameters
        ----------
        indices : list of int[3] or None
            sequence containing the indices of the objects that will be
            iterated. When the indices are provided, then the objects are
            returned in the same order the indices are returned by the
            iterable.
            If indices is None, then all objects are returned by the iterable
            and there is no restriction on the order that they are returned.

        Yields
        ------
        object : Node
            The Node item.

        Raises
        ------
        KeyError :
            if any of the indices passed as parameters are not in the dataset.
        """
        if item_type is not None and item_type != CUDSItem.NODE:
            raise ValueError("item_type must be CUDSItem.NODE")

        return self._iter_nodes(indices)

    def has(self, index):
        """iChecks if an object with the given index already exists
        in the dataset.

        Not implemented.
        """
        raise NotImplementedError()

    def has_type(self, item_type):
        """Checks if the specified CUDSItem type is present
        in the dataset.

        Not implemented
        """
        raise NotImplementedError()

    def __len__(self):
        """Returns the total number of items in the container.

        Returns
        -------
        count : int
            The number of items of item_type in the dataset.
        """
        return self.count_of(CUDSItem.NODE)

    @deprecated
    def get_node(self, index):  # pragma: no cover
        """
        Deprecated. Use get() instead.

        Get the lattice node corresponding to the given index.

        Parameters
        ----------
        index : int[3]
            node index coordinate

        Returns
        -------
        node : LatticeNode

        """
        return self.get(index)

    @deprecated
    def update_nodes(self, nodes):  # pragma: no cover
        """
        Deprecated. Use update() instead.

        Update the corresponding lattice nodes.

        Parameters
        ----------
        nodes : iterator of LatticeNodes

        """
        self.update(nodes)

    @deprecated
    def iter_nodes(self, indices=None):  # pragma: no cover
        """
        Deprecated. Use iter() instead.

        Get an iterator over the LatticeNodes described by the indices.

        Parameters
        ----------
        indices : iterable set of int[3], optional
            When indices (i.e. node index coordinates) are provided, then nodes
            are returned in the same order of the provided indices. If indices
            is None, there is no restriction on the order of the returned
            nodes.

        Returns
        -------
        iterator:
            An iterator over LatticeNode objects

        """
        return self.iter(indices)

    @property
    def primitive_cell(self):
        return self._primitive_cell

    def get_coordinate(self, ind):
        """Get coordinate of the given index coordinate.

        Parameters
        ----------
        ind : int[3]
            node index coordinate

        Returns
        -------
        coordinates : float[3]
        """
        p1 = self.primitive_cell.p1
        p2 = self.primitive_cell.p2
        p3 = self.primitive_cell.p3
        return (self.origin[0] + ind[0]*p1[0] + ind[1]*p2[0] + ind[2]*p3[0],
                self.origin[1] + ind[0]*p1[1] + ind[1]*p2[1] + ind[2]*p3[1],
                self.origin[2] + ind[0]*p1[2] + ind[1]*p2[2] + ind[2]*p3[2])

    @abstractmethod
    def _get_node(self, index):  # pragma: no cover
        pass

    @abstractmethod
    def _update_nodes(self, nodes):  # pragma: no cover
        pass

    @abstractmethod
    def _iter_nodes(self, indices=None):  # pragma: no cover
        pass
