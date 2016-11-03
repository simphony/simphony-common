from abc import abstractmethod

from simphony.core.cuds_item import CUDSItem
from simphony.cuds.abc_dataset import ABCDataset
from simphony.cuds.utils import deprecated


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
        return self._get_node(index)

    def add(self, iterable):
        raise NotImplementedError()

    def update(self, iterable):
        self._update_nodes(iterable)

    def remove(self, uids):
        raise NotImplementedError()

    def iter(self, uids=None, item_type=None):
        if item_type is not None and item_type != CUDSItem.NODE:
            raise ValueError("item_type must be CUDSItem.NODE")

        return self._iter_nodes(uids)

    def has(self, uid):
        raise NotImplementedError()

    def has_type(self, item_type):
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
