import itertools
from abc import abstractmethod

from simphony.core.cuds_item import CUDSItem
from simphony.cuds.abc_dataset import ABCDataset
from simphony.cuds.utils import deprecated

from simphony.cuds.mesh_items import Point, Edge, Face, Cell


class ABCMesh(ABCDataset):
    """Abstract base class for mesh.

    Attributes
    ----------
    name : str
        name of mesh
    """

    # Implements ABCDataset interface
    def get(self, uid):
        """Returns a copy of the object with the 'uid' id.

        Parameters
        ----------

        uid : uuid.UUID
            the uid of the object

        Raises
        ------
        KeyError :
            when the object is not in the container.

        Returns
        -------
        object :
            A copy of the internally stored info.
        """
        try:
            return self._get_point(uid)
        except KeyError:
            pass

        try:
            return self._get_edge(uid)
        except KeyError:
            pass

        try:
            return self._get_face(uid)
        except KeyError:
            pass

        try:
            return self._get_cell(uid)
        except KeyError:
            pass

        raise KeyError("Unknown uid {}".format(uid))

    def add(self, items):
        """Adds a set of objects from the provided iterable
        to the dataset.

        If any object has no uids, the dataset will generate a new
        uid for it. If the object has already an uid, it won't add the
        object if an object with the same type uid already exists.
        If the user wants to replace an existing object in the container
        there is an 'update' method for that purpose.

        Parameters
        ----------
        iterable : iterable of objects
            the new set of objects that will be included in the container.

        Returns
        -------
        uids : list of uuid.UUID
            The uids of the added objects.

        Raises
        ------
        ValueError :
            when there is an object with an uids that already exists
            in the dataset.
        """
        uids = []
        for item in items:
            if isinstance(item, Point):
                uids.extend(self._add_points([item]))
            elif isinstance(item, Edge):
                uids.extend(self._add_edges([item]))
            elif isinstance(item, Face):
                uids.extend(self._add_faces([item]))
            elif isinstance(item, Cell):
                uids.extend(self._add_cells([item]))
            else:
                raise TypeError(
                    "Unrecognised item type {!r}".format(item)
                )
        return uids

    def update(self, items):
        """Updates a set of objects from the provided iterable.

        Takes the uids of the objects and searches inside the dataset for
        those objects. If the object exists, they are replaced in the
        dataset. If any object doesn't exist, it will raise an exception.

        Parameters
        ----------

        iterable : iterable of objects
            the objects that will be replaced.

        Raises
        ------
        ValueError :
            If any object inside the iterable does not exist.
        """
        for item in items:
            if isinstance(item, Point):
                self._update_points([item])
            elif isinstance(item, Edge):
                self._update_edges([item])
            elif isinstance(item, Face):
                self._update_faces([item])
            elif isinstance(item, Cell):
                self._update_cells([item])
            else:
                raise TypeError(
                    "Unrecognised item type {!r}".format(item)
                )

    def remove(self, uids):
        """Remove the object with the provided uids from the container.

        The uids inside the iterable should exists in the container. Otherwise
        an exception will be raised.

        Parameters
        ----------
        uids : iterable of uuid.UUID
            the uids of the objects to be removed.

        Raises
        ------
        KeyError :
            If any object doesn't exist.
        """
        raise NotImplementedError("Remove is not implemented for Mesh")

    def iter(self, uids=None, item_type=None):
        """Generator method for iterating over the objects of the container.

        It can receive any kind of sequence of uids to iterate over
        those concrete objects. If nothing is passed as parameter, it will
        iterate over all the objects.

        Parameters
        ----------
        uids : iterable of uuid.UUID, optional
            sequence containing the uids of the objects that will be
            iterated. When the uids are provided, then the objects are
            returned in the same order the uids are returned by the iterable.
            If uids is None, then all objects are returned by the iterable
            and there is no restriction on the order that they are returned.

        item_type: CUDSItem
            Restricts the iteration to the specified type

        Yields
        ------
        object : Particle
            The object item.

        Raises
        ------
        KeyError :
            if any of the ids passed as parameters are not in the dataset.
        """
        if item_type == CUDSItem.POINT:
            return self._iter_points(uids)
        elif item_type == CUDSItem.EDGE:
            return self._iter_edges(uids)
        elif item_type == CUDSItem.FACE:
            return self._iter_faces(uids)
        elif item_type == CUDSItem.CELL:
            return self._iter_cells(uids)
        else:
            if uids is None:
                return itertools.chain(
                    self._iter_points(),
                    self._iter_edges(),
                    self._iter_faces(),
                    self._iter_cells(),
                )
            else:
                return self._iter_uids(uids)

    def has(self, uid):
        """Checks if an object with the given uid already exists
        in the dataset.

        Parameters
        ----------
        uid : uuid.UUID
            the uid of the object

        Returns
        -------
        True if the uid is found, False otherwise.
        """
        try:
            self.get(uid)
        except KeyError:
            return False

        return True

    def has_type(self, item_type):
        """Checks if the specified CUDSItem type is present
        in the dataset.

        Parameters
        ----------
        item_type : CUDSItem
            The CUDSItem enum of the type.

        Returns
        -------
        True if the type is present, False otherwise.
        """
        if item_type == CUDSItem.POINT:
            return self._has_points()
        elif item_type == CUDSItem.EDGE:
            return self._has_edges()
        elif item_type == CUDSItem.FACE:
            return self._has_faces()
        elif item_type == CUDSItem.CELL:
            return self._has_cells()
        else:
            raise ValueError("Unknown item_type "
                             "{}".format(item_type))

    # Deprecated methods.

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

    # Private. Need to be reimplemented by subclasses
    #
    # These methods documented behavior is as the deprecated
    # variants above. They are used temporarily as a shim to expose
    # the old interface through the new one without too many changes.

    @abstractmethod
    def _get_point(self, uid):  # pragma: no cover
        pass

    @abstractmethod
    def _get_edge(self, uid):  # pragma: no cover
        pass

    @abstractmethod
    def _get_face(self, uid):  # pragma: no cover
        pass

    @abstractmethod
    def _get_cell(self, uid):  # pragma: no cover
        pass

    @abstractmethod
    def _add_points(self, points):  # pragma: no cover
        pass

    @abstractmethod
    def _add_edges(self, edges):  # pragma: no cover
        pass

    @abstractmethod
    def _add_faces(self, faces):  # pragma: no cover
        pass

    @abstractmethod
    def _add_cells(self, cells):  # pragma: no cover
        pass

    @abstractmethod
    def _update_points(self, points):  # pragma: no cover
        pass

    @abstractmethod
    def _update_edges(self, edges):  # pragma: no cover
        pass

    @abstractmethod
    def _update_faces(self, faces):  # pragma: no cover
        pass

    @abstractmethod
    def _update_cells(self, cells):  # pragma: no cover
        pass

    @abstractmethod
    def _iter_points(self, uids=None):  # pragma: no cover
        pass

    @abstractmethod
    def _iter_edges(self, uids=None):  # pragma: no cover
        pass

    @abstractmethod
    def _iter_faces(self, uids=None):  # pragma: no cover
        pass

    @abstractmethod
    def _iter_cells(self, uids=None):  # pragma: no cover
        pass

    @abstractmethod
    def _has_points(self):  # pragma: no cover
        pass

    @abstractmethod
    def _has_edges(self):  # pragma: no cover
        pass

    @abstractmethod
    def _has_faces(self):  # pragma: no cover
        pass

    @abstractmethod
    def _has_cells(self):  # pragma: no cover
        pass

    # Private, with implementation

    def _iter_uids(self, uids):
        """Iterates over a series of uids

        Parameters
        ----------
        uids: iterable
            iterable with the uids to return

        Yields
        ------
        The items corresponding to the uids.
        """
        for uid in uids:
            yield self.get(uid)
