from simphony.core.cuds_item import CUDSItem
from simphony.cuds.abc_dataset import ABCDataset
from simphony.cuds.utils import deprecated


class ABCMesh(ABCDataset):
    """Abstract base class for mesh.

    Attributes
    ----------
    name : str
        name of mesh
    """

    @deprecated
    def get_point(self, uid):  # pragma: no cover
        """
        Deprecated. Use get() instead.

        Returns a point with a given uid.

        Returns the point stored in the mesh
        identified by uid. If such point do not
        exists an exception is raised.

        Parameters
        ----------
        uid : uuid.UUID
            uid of the desired point.

        Returns
        -------
        point : Point
            Mesh point identified by uuid

        Raises
        ------
        KeyError :
            If the point identified by uid was not found
        TypeError :
            When ``uid`` is not uuid.UUID

        """
        return self.get(uid)

    @deprecated
    def get_edge(self, uid):  # pragma: no cover
        """ Returns an edge with a given uid.

        Returns the edge stored in the mesh
        identified by uid. If such edge do not
        exists an exception is raised.

        Parameters
        ----------
        uid : uuid.UUID
            uid of the desired edge.

        Returns
        -------
        edge : Edge
            Edge identified by uid

        Raises
        ------
        KeyError :
            If the edge identified by uid was not found
        TypeError :
            When ``uid`` is not uuid.UUID

        """
        return self.get(uid)

    @deprecated
    def get_face(self, uid):  # pragma: no cover
        """
        Deprecated. Use get() instead.

        Returns a face with a given uid.

        Returns the face stored in the mesh
        identified by uid. If such a face does
        not exists an exception is raised.

        Parameters
        ----------
        uid : uuid.UUID
            uid of the desired face.

        Returns
        -------
        face : Face
            Face identified by uid

        Raises
        ------
        KeyError :
            If the face identified by uid was not found
        TypeError :
            When ``uid`` is not uuid.UUID
        """
        return self.get(uid)

    @deprecated
    def get_cell(self, uid):  # pragma: no cover
        """
        Deprecated. Use get() instead.

        Returns a cell with a given uid.

        Returns the cell stored in the mesh
        identified by uid. If such a cell does not
        exists an exception is raised.

        Parameters
        ----------
        uid : uuid.UUID
            uid of the desired cell.

        Returns
        -------
        cell : Cell
            Cell identified by uid

        Raises
        ------
        KeyError :
            If the cell identified by uuid was not found
        TypeError :
            When ``uid`` is not uuid.UUID
        """
        return self.get(uid)

    @deprecated
    def add_points(self, points):  # pragma: no cover
        """
        Deprecated. use add() instead.

        Adds a set of new points to the mesh.

        Parameters
        ----------
        points : iterable of Point
            Points to be added to the mesh

        Raises
        ------
        ValueError :
            If other point with a duplicated uid was already
            in the mesh.
        """
        return self.add(points)

    @deprecated
    def add_edges(self, edges):
        """
        Deprecated. Use add() instead.

        Adds a set of new edges to the mesh.

        Parameters
        ----------
        edges : iterable of Edge
            Edge to be added to the mesh

        Raises
        ------
        ValueError :
            If other edge with a duplicated uid was already
            in the mesh
        """
        return self.add(edges)

    @deprecated
    def add_faces(self, faces):  # pragma: no cover
        """
        Deprecated. Use add() instead.

        Adds a set of new faces to the mesh.

        Parameters
        ----------
        faces : iterable of Face
            Face to be added to the mesh

        Raises
        ------
        ValueError :
            If other face with a duplicated uid was already
            in the mesh
        """
        return self.add(faces)

    @deprecated
    def add_cells(self, cells):  # pragma: no cover
        """
        Deprecated. Use add() instead.

        Adds a set of new cells to the mesh.

        Parameters
        ----------
        cells : iterable of Cell
            Cell to be added to the mesh

        Raises
        ------
        ValueError :
            If other cell with a duplicated uid was already
            in the mesh
        """
        return self.add(cells)

    @deprecated
    def update_points(self, points):  # pragma: no cover
        """
        Deprecated. Use update() instead.

        Updates the information of a set of points.

        Gets the mesh point identified by the same
        uid as the provided point and updates its information
        with the one provided with the new point.

        Parameters
        ----------
        points : iterable of Point
            Point to be updated

        Raises
        ------
        ValueError :
            If the any point was not found in the mesh
        """
        self.update(points)

    @deprecated
    def update_edges(self, edges):  # pragma: no cover
        """
        Deprecated. Use update() instead.

        Updates the information of a set of edges.

        Gets the mesh edge identified by the same
        uid as the provided edge and updates its information
        with the one provided with the new edge.

        Parameters
        ----------
        edges : iterable of Edge
            Edge to be updated

        Raises
        ------
        ValueError :
            If the any edge was not found in the mesh
        """
        self.update(edges)

    @deprecated
    def update_faces(self, faces):  # pragma: no cover
        """
        Deprecated. Use update() instead.

        Updates the information of a set of faces.

        Gets the mesh face identified by the same
        uid as the provided face and updates its information
        with the one provided with the new face.

        Parameters
        ----------
        faces : iterable of Face
            Face to be updated

        Raises
        ------
        ValueError :
            If the any face was not found in the mesh
        """
        self.update(faces)

    @deprecated
    def update_cells(self, cells):  # pragma: no cover
        """
        Deprecated. Use update() instead.

        Updates the information of a set of cells.

        Gets the mesh cell identified by the same
        uid as the provided cell and updates its information
        with the one provided with the new cell.

        Parameters
        ----------
        cells : iterable of Cell
            Cell to be updated

        Raises
        ------
        ValueError :
            If the any cell was not found in the mesh
        """
        self.update(cells)

    @deprecated
    def iter_points(self, uids=None):  # pragma: no cover
        """
        Deprecated. Use iter() instead.

        Returns an iterator over points.

        Parameters
        ----------
        uids : iterable of uuid.UUID  or None
            When the uids are provided, then the points are returned in the
            same order the uids are returned by the iterable. If uids is None,
            then all points are returned by the iterable and there is no
            restriction on the order that they are returned.

        Yields
        ------
        point : Point
        """
        return self.iter(uids, CUDSItem.POINT)

    @deprecated
    def iter_edges(self, uids=None):  # pragma: no cover
        """
        Deprecated. Use iter() instead.

        Returns an iterator over edges.

        Parameters
        ----------
        uids : iterable of uuid.UUID  or None
            When the uids are provided, then the edges are returned in the same
            order the uids are returned by the iterable. If uids is None, then
            all edges are returned by the iterable and there is no restriction
            on the order that they are returned.

        Yields
        ------
        edge : Edge

        """
        return self.iter(uids, CUDSItem.EDGE)

    @deprecated
    def iter_faces(self, uids=None):  # pragma: no cover
        """
        Deprecated. Use iter() instead.

        Returns an iterator over faces.

        Parameters
        ----------
        uids : iterable of uuid.UUID  or None
            When the uids are provided, then the faces are returned in the same
            order the uids are returned by the iterable. If uids is None, then
            all faces are returned by the iterable and there is no restriction
            on the order that they are returned.

        Yields
        ------
        face : Face

        """
        return self.iter(uids, item_type=CUDSItem.FACE)

    @deprecated
    def iter_cells(self, uids=None):  # pragma: no cover
        """
        Deprecated. Use iter() instead.

        Returns an iterator over cells.

        Parameters
        ----------
        uids : iterable of uuid.UUID  or None
            When the uids are provided, then the cells are returned in the same
            order the uids are returned by the iterable. If uids is None, then
            all cells are returned by the iterable and there is no restriction
            on the order that they are returned.

        Yields
        ------
        cell : Cell

        """
        return self.iter(uids, item_type=CUDSItem.CELL)

    @deprecated
    def has_points(self):  # pragma: no cover
        """ Check if the mesh has points

        Returns
        -------
        result : bool
            True of there are points inside the mesh,
            False otherwise
        """
        return self.has_type(CUDSItem.POINT)

    @deprecated
    def has_edges(self):  # pragma: no cover
        """ Check if the mesh has edges

        Returns
        -------
        result : bool
            True of there are edges inside the mesh,
            False otherwise
        """
        return self.has_type(CUDSItem.EDGE)

    @deprecated
    def has_faces(self):  # pragma: no cover
        """ Check if the mesh has faces

        Returns
        -------
        result : bool
            True of there are faces inside the mesh,
            False otherwise
        """
        return self.has_type(CUDSItem.FACE)

    @deprecated
    def has_cells(self):  # pragma: no cover
        """ Check if the mesh has cells

        Returns
        -------
        result : bool
            True of there are cells inside the mesh,
            False otherwise
        """
        return self.has_type(CUDSItem.CELL)
