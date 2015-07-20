from abc import ABCMeta, abstractmethod


class ABCMesh(object):
    """Abstract base class for mesh.

    Attributes
    ----------
    name : str
        name of mesh

    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_point(self, uid):
        """ Returns a point with a given uid.

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

    @abstractmethod
    def get_edge(self, uid):
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

    @abstractmethod
    def get_face(self, uid):
        """ Returns a face with a given uid.

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

    @abstractmethod
    def get_cell(self, uid):
        """ Returns a cell with a given uid.

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

    @abstractmethod
    def add_points(self, points):
        """ Adds a set of new points to the mesh.

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

    @abstractmethod
    def add_edges(self, edge):
        """ Adds a set of new edges to the mesh.

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

    @abstractmethod
    def add_faces(self, face):
        """ Adds a set of new faces to the mesh.

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

    @abstractmethod
    def add_cells(self, cell):
        """ Adds a set of new cells to the mesh.

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

    @abstractmethod
    def update_points(self, point):
        """ Updates the information of a set of points.

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

    @abstractmethod
    def update_edges(self, edge):
        """ Updates the information of a set of edges.

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

    @abstractmethod
    def update_faces(self, face):
        """ Updates the information of a set of faces.

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

    @abstractmethod
    def update_cells(self, cell):
        """ Updates the information of a set of cells.

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

    @abstractmethod
    def iter_points(self, uids=None):
        """ Returns an iterator over points.

        Parameters
        ----------
        uids : iterable of uuid.UUID  or None
            When the uids are provided, then the points are returned in the
            same order the uids are returned by the iterable. If uids is None,
            then all points are returned by the interable and there is no
            restriction on the order that they are returned.

        Yields
        ------
        point : Point

        """

    @abstractmethod
    def iter_edges(self, uids=None):
        """ Returns an iterator over edges.

        Parameters
        ----------
        uids : iterable of uuid.UUID  or None
            When the uids are provided, then the edges are returned in the same
            order the uids are returned by the iterable. If uids is None, then
            all edges are returned by the interable and there is no restriction
            on the order that they are returned.

        Yields
        ------
        edge : Edge

        """

    @abstractmethod
    def iter_faces(self, uids=None):
        """ Returns an iterator over faces.

        Parameters
        ----------
        uids : iterable of uuid.UUID  or None
            When the uids are provided, then the faces are returned in the same
            order the uids are returned by the iterable. If uids is None, then
            all faces are returned by the interable and there is no restriction
            on the order that they are returned.

        Yields
        ------
        face : Face

        """

    @abstractmethod
    def iter_cells(self, uids=None):
        """ Returns an iterator over cells.

        Parameters
        ----------
        uids : iterable of uuid.UUID  or None
            When the uids are provided, then the cells are returned in the same
            order the uids are returned by the iterable. If uids is None, then
            all cells are returned by the interable and there is no restriction
            on the order that they are returned.

        Yields
        ------
        cell : Cell

        """

    @abstractmethod
    def has_edges(self):
        """ Check if the mesh has edges

        Returns
        -------
        result : bool
            True of there are edges inside the mesh,
            False otherwise

        """

    @abstractmethod
    def has_faces(self):
        """ Check if the mesh has faces

        Returns
        -------
        result : bool
            True of there are faces inside the mesh,
            False otherwise

        """

    @abstractmethod
    def has_cells(self):
        """ Check if the mesh has cells

        Returns
        -------
        result : bool
            True of there are cells inside the mesh,
            False otherwise

        """

    @abstractmethod
    def count_of(self, item_type):
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
