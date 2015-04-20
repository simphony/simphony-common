""" Mesh module

This module contains the implementation to store, access,
and modify a mesh

"""
import uuid
from abstractmesh import ABCMesh
import simphony.core.data_container as dc


class Point(object):
    """ Coordinates describing a point in the space

    Set of coordinates(x,y,z) describing a point in
    the space and data about that point

    Parameters
    ----------
    uid :
        uid of the point.
    coordinates : list of double
        set of coordinates (x,y,z) describing the point position.
    data : DataContainer
        object to store point data

    Attributes
    ----------
    uid :
        uuid of the point.
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
    uid :
        uuid of the element
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

    @classmethod
    def from_element(cls, element):
        return cls(
            element.points,
            element.uid,
            element.data
        )


class Edge(Element):
    """ Edge element

    Element for storing 1D geometrical objects

    Parameters
    ----------
    points : list of uid
        list of points uids defining the edge.
    uid :
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
    uid :
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
    uid :
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

    (1) methods to get the related item with the provided uuid;
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

    See Also
    --------
    get_point, get_edge, get_face, get_cell
    add_point, add_edge, add_face, add_cell
    update_point, update_edge, update_face, update_cell
    iter_points, iter_edges, iter_faces, iter_cells
    has_edges, has_faces, has_cells

    """

    def __init__(self, name):
        self.name = name

        self._points = {}
        self._edges = {}
        self._faces = {}
        self._cells = {}

        self._data = dc.DataContainer()

    @property
    def data(self):
        return dc.DataContainer(self._data)

    @data.setter
    def data(self, value):
        self._data = dc.DataContainer(value)

    def get_point(self, uid):
        """ Returns a point with a given uuid.

        Returns the point stored in the mesh
        identified by uuid. If such point do not
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
            If the point identified by uuid was not found
        TypeError :
            When ``uid`` is not uuid.UUID

        """
        if isinstance(uid, uuid.UUID):
            return Point.from_point(self._points[uid])
        else:
            message = 'Expected type for `uid` is uuid.UUID but received {!r}'
            raise TypeError(message.format(type(uid)))


    def get_edge(self, uid):
        """ Returns an edge with a given uuid.

        Returns the edge stored in the mesh
        identified by uuid. If such edge do not
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
            If the edge identified by uuid was not found
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
        identified by uid. If such face do not
        exists an exception is raised.

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
            If the face identified by uuid was not found
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
        identified by uuid . If such cell do not
        exists an exception is raised.

        Parameters
        ----------
        uid : uuid.UUID
            uid of the desired cell.

        Returns
        -------
        cell : Cell
            Cell with id identified by uid

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

    def add_point(self, point):
        """ Adds a new point to the mesh.

        Parameters
        ----------
        point : Point
            Point to be added to the mesh

        Raises
        ------
        KeyError :
            If other point with the same uid was already
            in the mesh

        """
        if point.uid is None:
            point.uid = self._generate_uuid()
        elif point.uid in self._points:
            error_str = "Trying to add an already existing point with uuid: {}"
            raise ValueError(error_str.format(point.uid))

        self._points[point.uid] = Point.from_point(point)

        return point.uid

    def add_edge(self, edge):
        """ Adds a new edge to the mesh.

        Parameters
        ----------
        edge : Edge
            Edge to be added to the mesh

        Raises
        ------
        KeyError :
            If other edge with the same uid was already
            in the mesh

        """

        if edge.uid is None:
            edge.uid = self._generate_uuid()
        elif edge.uid in self._edges:
            error_str = "Trying to add an already existing edge with uuid: {}"
            raise ValueError(error_str.format(edge.uid))

        self._edges[edge.uid] = Edge.from_edge(edge)

        return edge.uid

    def add_face(self, face):
        """ Adds a new face to the mesh.

        Parameters
        ----------
        face : Face
            Face to be added to the mesh

        Raises
        ------
        ValueError
            If other face with the same uid was already
            in the mesh

        """
        if face.uid is None:
            face.uid = self._generate_uuid()
        elif face.uid in self._faces:
            error_str = "Trying to add an already existing face with uuid: {}"
            raise ValueError(error_str.format(face.uid))

        self._faces[face.uid] = Face.from_face(face)

        return face.uid

    def add_cell(self, cell):
        """ Adds a new cell to the mesh.

        Parameters
        ----------
        cell : Cell
            Cell to be added to the mesh

        Raises
        ------
        KeyError
            If other cell with the same uid was already
            in the mesh

        TypeError
            If the object provided is not a cell

        """

        if cell.uid is None:
            cell.uid = self._generate_uuid()
        elif cell.uid in self._cells:
            error_str = "Trying to add an already existing cell with uuid: {}"
            raise ValueError(error_str.format(cell.uid))
        self._cells[cell.uid] = Cell.from_cell(cell)
        return cell.uid

    def update_point(self, point):
        """ Updates the information of a point.

        Gets the mesh point identified by the same
        id as the provided point and updates its information
        with the one provided with the new point.

        Parameters
        ----------
        point : Point
            Point to be updated

        Raises
        ------
        KeyError
            If the point was not found in the mesh

        """
        if point.uid not in self._points:
            error_str = "Trying to update a non-existing point with uid: {}"
            raise ValueError(error_str.format(point.uid))

        point_to_update = self._points[point.uid]
        point_to_update.data = point.data
        point_to_update.coordinates = point.coordinates

    def update_edge(self, edge):
        """ Updates the information of an edge.

        Gets the mesh edge identified by the same
        id as the provided edge and updates its information
        with the one provided with the new edge.

        Parameters
        ----------
        edge : Edge
            Edge to be updated

        Raises
        ------
        KeyError
            If the edge was not found in the mesh

        """
        if edge.uid not in self._edges:
            error_str = "Trying to update a non-existing edge with uid: {}"
            raise ValueError(error_str.format(edge.uid))

        edge_to_update = self._edges[edge.uid]
        edge_to_update.data = edge.data
        edge_to_update.points = edge.points

    def update_face(self, face):
        """ Updates the information of a face.

        Gets the mesh face identified by the same
        uuid as the provided face and updates its information
        with the one provided with the new face.

        Parameters
        ----------
        face : Face
            Face to be updated

        Raises
        ------
        KeyError
            If the face was not found in the mesh

        """

        if face.uid not in self._faces:
            error_str = "Trying to update a non-existing face with uid: {}"
            raise ValueError(error_str.format(face.uid))

        face_to_update = self._faces[face.uid]

        face_to_update.data = face.data
        face_to_update.points = face.points

    def update_cell(self, cell):
        """ Updates the information of a cell.

        Gets the mesh cell identified by the same
        uuid as the provided cell and updates its information
        with the one provided with the new cell.

        Parameters
        ----------
        cell : Cell
            Cell to be updated

        Raises
        ------
        KeyError :
            If the cell was not found in the mesh

        """
        if cell.uid not in self._cells:
            error_str = "Trying to update a non-existing cell with uid: {}"
            raise ValueError(error_str.format(cell.uid))

        cell_to_update = self._cells[cell.uid]
        cell_to_update.data = cell.data
        cell_to_update.points = cell.points

    def iter_points(self, point_uids=None):
        """ Returns an iterator over the selected points.

        Returns an iterator over the points with uid in
        point_uids. If none of the ids in point_uids exists,
        an empty iterator is returned. If there is no ids
        inside point_uids, a iterator over all points of
        the mesh is returned instead.

        Parameters
        ----------
        point_uids : list of uid, optional
            uids of the desired points, default empty

        Yields
        ------
        cell : Cell

        """
        if point_uids is None:
            for point in self._points.values():
                yield Point.from_point(point)
        else:
            for point_uid in point_uids:
                yield Point.from_point(self._points[point_uid])

    def iter_edges(self, edge_uids=None):
        """ Returns an iterator over the selected edges.

        Returns an iterator over the edged with uid in
        edge_uid. If none of the uids in edge_uids exists,
        an empty iterator is returned. If there is no uids
        inside edge_uids, a iterator over all edges of
        the mesh is returned instead.

        Parameters
        ----------
        edge_uids : list of uid, optional
            uids of the desired edges, default empty

        Yields
        ------
        edge : Edge

        """

        if edge_uids is None:
            for edge in self._edges.values():
                yield Edge.from_edge(edge)
        else:
            for edge_uid in edge_uids:
                yield Edge.from_edge(self._edges[edge_uid])

    def iter_faces(self, face_uids=None):
        """ Returns an iterator over the selected faces.

        Returns an iterator over the faces with uid in
        face_uids. If none of the uuids in face_uids exists,
        an empty iterator is returned. If there is no uids
        inside face_uids, a iterator over all faces of
        the mesh is returned instead.

        Parameters
        ----------
        face_uids : list of uid, optional
            uids of the desired faces, default empty

        Yields
        ------
        face : Face

        """
        if face_uids is None:
            for face in self._faces.values():
                yield Face.from_face(face)
        else:
            for face_uid in face_uids:
                yield Face.from_face(self._faces[face_uid])

    def iter_cells(self, cell_uids=None):
        """ Returns an iterator over the selected cells.

        Returns an iterator over the cells with uid in
        cell_uids. If none of the uids in cell_uids exists,
        an empty iterator is returned. If there is no uuids
        inside cell_uuids, a iterator over all cells of
        the mesh is returned instead.

        Parameters
        ----------
        cell_uids : list of uid, optional
            uids of the desired cell, default empty

        Yields
        ------
        cell : Cell

        """
        if cell_uids is None:
            for cell in self._cells.values():
                yield Cell.from_cell(cell)
        else:
            for cell_uid in cell_uids:
                yield Cell.from_cell(self._cells[cell_uid])

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

    def _generate_uuid(self):
        """ Provides and uuid for the object

        Provides san uuid as defined in the standard RFC 4122
        """
        return uuid.uuid4()
