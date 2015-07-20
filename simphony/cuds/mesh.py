""" Mesh module

This module contains the implementation to store, access,
and modify a mesh

"""
import uuid
from simphony.cuds.abstractmesh import ABCMesh
from simphony.core.cuds_item import CUDSItem
import simphony.core.data_container as dc


class Point(object):
    """ Coordinates describing a point in the space

    Set of coordinates (x,y,z) describing a point in
    the space and data about that point

    Parameters
    ----------
    uid : uuid.UUID
        uid of the point.
    coordinates : list of double
        set of coordinates (x,y,z) describing the point position.
    data : DataContainer
        object to store point data

    Attributes
    ----------
    uid : uuid.UUID
        uid of the point.
    data : DataContainer
        object to store point data
    coordinates : list of double
        set of coordinates (x,y,z) describing the point position.

    """

    def __init__(self, coordinates, uid=None, data=None):
        self.uid = uid
        self.coordinates = tuple(coordinates)

        if data:
            self.data = dc.DataContainer(data)
        else:
            self.data = dc.DataContainer()

    @classmethod
    def from_point(cls, point):
        return cls(
            point.coordinates,
            point.uid,
            point.data
        )


class Element(object):
    """ Element base class

    Element for storing geometrical objects

    Parameters
    ----------
    uid :
        uid of the edge.
    points : list of uid
        list of points uids defining the edge.
    data : DataContainer
        object to store data relative to the element

    Attributes
    ----------
    points : list of uid
        list of points uids defining the element.
    uid : uuid.UUID
        uid of the element
    data : DataContainer
        Element data

    """

    def __init__(self, points, uid=None, data=None):
        self.uid = uid
        self.points = points[:]

        if data:
            self.data = dc.DataContainer(data)
        else:
            self.data = dc.DataContainer()


class Edge(Element):
    """ Edge element

    Element for storing 1D geometrical objects

    Parameters
    ----------
    points : list of uid
        list of points uids defining the edge.
    uid : uuid.UUID
        uid of the edge.
    data : DataContainer
        object to store data relative to the edge

    """

    @classmethod
    def from_edge(cls, edge):
        return cls(
            edge.points,
            edge.uid,
            edge.data
        )


class Face(Element):
    """ Face element

    Element for storing 2D geometrical objects

    Parameters
    ----------
    points : list of uid
        list of points uids defining the face.
    uid : uuid.UUID
        uid of the face.
    data : DataContainer
        object to store data relative to the face

    """

    @classmethod
    def from_face(cls, face):
        return cls(
            face.points,
            face.uid,
            face.data
        )


class Cell(Element):
    """ Cell element

    Element for storing 3D geometrical objects

    Parameters
    ----------
    points : list of uid
        list of points uids defining the cell.
    uid : uuid.UUID
        uid of the cell.
    data : DataContainer
        object to store data relative to the cell

    """

    @classmethod
    def from_cell(cls, cell):
        return cls(
            cell.points,
            cell.uid,
            cell.data
        )


class Mesh(ABCMesh):
    """ Mesh object to store points and elements.

    Stores general mesh information Points and Elements
    such as Edges, Faces and Cells and provide the
    methods to interact with them. The methods are
    divided in four different blocks:

    (1) methods to get the related item with the provided uid;
    (2) methods to add a new item or replace;
    (3) generator methods that return iterators
        over all or some of the mesh items and;
    (4) inspection methods to identify if there are any edges,
        faces or cells described in the mesh.

    Parameters
    ----------
    name : str
        name of mesh

    Attributes
    ----------
    name : str
        name of mesh
    data : Data
        Data relative to the mesh.
    points : dictionary of Point
        Points of the mesh.
    edges : dictionary of Edge
        Edges of the mesh.
    faces : dictionary of Face
        Faces of the mesh.
    cells : dictionary of Cell
        Cells of the mesh.

    """

    def __init__(self, name):
        self.name = name

        self._points = {}
        self._edges = {}
        self._faces = {}
        self._cells = {}

        self._data = dc.DataContainer()

        self._items_count = {
            CUDSItem.POINT: lambda: self._points,
            CUDSItem.EDGE: lambda: self._edges,
            CUDSItem.FACE: lambda: self._faces,
            CUDSItem.CELL: lambda: self._cells
        }

    @property
    def data(self):
        return dc.DataContainer(self._data)

    @data.setter
    def data(self, value):
        self._data = dc.DataContainer(value)

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
        if isinstance(uid, uuid.UUID):
            return Point.from_point(self._points[uid])
        else:
            message = 'Expected type for `uid` is uuid.UUID but received {!r}'
            raise TypeError(message.format(type(uid)))

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
        if isinstance(uid, uuid.UUID):
            return Edge.from_edge(self._edges[uid])
        else:
            message = 'Expected type for `uid` is uuid.UUID but received {!r}'
            raise TypeError(message.format(type(uid)))

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
        if isinstance(uid, uuid.UUID):
            return Face.from_face(self._faces[uid])
        else:
            message = 'Expected type for `uid` is uuid.UUID but received {!r}'
            raise TypeError(message.format(type(uid)))

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
        if isinstance(uid, uuid.UUID):
            return Cell.from_cell(self._cells[uid])
        else:
            message = 'Expected type for `uid` is uuid.UUID but received {!r}'
            raise TypeError(message.format(type(uid)))

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
        rpoints = []
        for point in points:
            if point.uid is None:
                point.uid = self._generate_uuid()
            elif point.uid in self._points:
                err_str = "Trying to add an already existing \
                    point with uuid: {}"
                raise ValueError(err_str.format(point.uid))

            self._points[point.uid] = Point.from_point(point)

            rpoints.append(point.uid)
        return rpoints

    def add_edges(self, edges):
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
        redges = []
        for edge in edges:
            if edge.uid is None:
                edge.uid = self._generate_uuid()
            elif edge.uid in self._edges:
                err_str = "Trying to add an already existing \
                    edge with uuid: {}"
                raise ValueError(err_str.format(edge.uid))

            self._edges[edge.uid] = Edge.from_edge(edge)

            redges.append(edge.uid)
        return redges

    def add_faces(self, faces):
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
        rfaces = []
        for face in faces:
            if face.uid is None:
                face.uid = self._generate_uuid()
            elif face.uid in self._faces:
                err_str = "Trying to add an already existing \
                    face with uuid: {}"
                raise ValueError(err_str.format(face.uid))

            self._faces[face.uid] = Face.from_face(face)

            rfaces.append(face.uid)
        return rfaces

    def add_cells(self, cells):
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
        rcells = []
        for cell in cells:
            if cell.uid is None:
                cell.uid = self._generate_uuid()
            elif cell.uid in self._cells:
                err_str = "Trying to add an already existing \
                    cell with uuid: {}"
                raise ValueError(err_str.format(cell.uid))

            self._cells[cell.uid] = Cell.from_cell(cell)
            rcells.append(cell.uid)
        return rcells

    def update_points(self, points):
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
        for point in points:
            if point.uid not in self._points:
                err_str = "Trying to update a non-existing point with uid: {}"
                raise ValueError(err_str.format(point.uid))

            point_to_update = self._points[point.uid]
            point_to_update.data = point.data
            point_to_update.coordinates = point.coordinates

    def update_edges(self, edges):
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
        for edge in edges:
            if edge.uid not in self._edges:
                err_str = "Trying to update a non-existing edge with uid: {}"
                raise ValueError(err_str.format(edge.uid))

            edge_to_update = self._edges[edge.uid]
            edge_to_update.data = edge.data
            edge_to_update.points = edge.points

    def update_faces(self, faces):
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
        for face in faces:
            if face.uid not in self._faces:
                err_str = "Trying to update a non-existing face with uid: {}"
                raise ValueError(err_str.format(face.uid))

            face_to_update = self._faces[face.uid]
            face_to_update.data = face.data
            face_to_update.points = face.points

    def update_cells(self, cells):
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
        for cell in cells:
            if cell.uid not in self._cells:
                err_str = "Trying to update a non-existing cell with uid: {}"
                raise ValueError(err_str.format(cell.uid))

            cell_to_update = self._cells[cell.uid]
            cell_to_update.data = cell.data
            cell_to_update.points = cell.points

    def iter_points(self, uids=None):
        """ Returns an iterator over points.

        Parameters
        ----------
        uids : iterable of uuid.UUID or None
            When the uids are provided, then the points are returned in
            the same order the uids are returned by the iterable. If uids is
            None, then all points are returned by the interable and there
            is no restriction on the order that they are returned.

        Yields
        ------
        cell : Cell

        """
        if uids is None:
            for point in self._points.values():
                yield Point.from_point(point)
        else:
            for point_uid in uids:
                yield Point.from_point(self._points[point_uid])

    def iter_edges(self, uids=None):
        """ Returns an iterator over edges.

        Parameters
        ----------
        uids : iterable of uuid.UUID  or None
            When the uids are provided, then the edges are returned in the
            same order the uids are returned by the iterable. If uids is None,
            then all edges are returned by the interable and there is no
            restriction on the order that they are returned.

        Yields
        ------
        edge : Edge

        """

        if uids is None:
            for edge in self._edges.values():
                yield Edge.from_edge(edge)
        else:
            for uid in uids:
                yield Edge.from_edge(self._edges[uid])

    def iter_faces(self, uids=None):
        """ Returns an iterator over faces.

        Parameters
        ----------
        uids : iterable of uuid.UUID  or None
            When the uids are provided, then the faces are returned in the
            same order the uids are returned by the iterable. If uids is None,
            then all faces are returned by the interable and there is no
            restriction on the order that they are returned.

        Yields
        ------
        face : Face

        """
        if uids is None:
            for face in self._faces.values():
                yield Face.from_face(face)
        else:
            for uid in uids:
                yield Face.from_face(self._faces[uid])

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
        if uids is None:
            for cell in self._cells.values():
                yield Cell.from_cell(cell)
        else:
            for uid in uids:
                yield Cell.from_cell(self._cells[uid])

    def has_edges(self):
        """ Check if the mesh has edges

        Returns
        -------
        result  : bool
            True of there are edges inside the mesh,
            False otherwise

        """
        return len(self._edges) > 0

    def has_faces(self):
        """ Check if the mesh has faces

        Returns
        -------
        result : bool
            True of there are faces inside the mesh,
            False otherwise

        """
        return len(self._faces) > 0

    def has_cells(self):
        """ Check if the mesh has cells

        Returns
        -------
        result : bool
            True of there are cells inside the mesh,
            False otherwise

        """
        return len(self._cells) > 0

    def count_of(self, item_type):
        """ Return the count of item_type in the container.

        Parameter
        ---------
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

        try:
            return len(self._items_count[item_type]())
        except KeyError:
            error_str = "Trying to obtain count a of non-supported item: {}"
            raise ValueError(error_str.format(item_type))

    def _generate_uuid(self):
        """ Provides a uuid for the object

        Provides a uuid as defined in the standard RFC 4122
        """
        return uuid.uuid4()
