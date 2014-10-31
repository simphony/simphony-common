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
    uuid :
        uuid of the point.
    coordinates : list of double
        set of coordinates (x,y,z) describing the point position.
    data : DataContainer
        object to store point data

    Attributes
    ----------
    uuid :
        uuid of the point.
    data : DataContainer
        object to store point data
    coordinates : list of double
        set of coordinates (x,y,z) describing the point position.

    """

    def __init__(self, coordinates, uuid=None, data=None):
        self.uuid = uuid
        self.coordinates = tuple(coordinates)

        if data:
            self.data = dc.DataContainer(data)
        else:
            self.data = dc.DataContainer()

    @classmethod
    def from_point(cls, point):
        return cls(
            point.coordinates,
            point.uuid,
            point.data
        )


class Element(object):
    """ Element base class

    Element for storing geometrical objects

    Parameters
    ----------
    uuid :
        uuid of the edge.
    points : list of Point
        list of points defining the edge.
    data : DataContainer
        object to store data relative to the element

    Attributes
    ----------
    uuid :
        uuid of the element
    data : DataContainer
        Element data
    points : list of Point
        list of points defining the element.

    """

    def __init__(self, points, uuid=None, data=None):
        self.uuid = uuid
        self.points = points[:]

        if data:
            self.data = dc.DataContainer(data)
        else:
            self.data = dc.DataContainer()

    @classmethod
    def from_element(cls, element):
        return cls(
            element.points,
            element.uuid,
            element.data
        )


class Edge(Element):
    """ Edge element

    Element for storing 1D geometrical objects

    Parameters
    ----------
    uuid :
        uuid of the edge.
    points : list of Point
        list of points defining the edge.
    data : DataContainer
        object to store data relative to the edge

    """

    @classmethod
    def from_edge(cls, edge):
        return cls(
            edge.points,
            edge.uuid,
            edge.data
        )


class Face(Element):
    """ Face element

    Element for storing 2D geometrical objects

    Parameters
    ----------
    uuid :
        uuid of the face.
    points: list of Point
        list of points defining the face.
    data: DataContainer
        object to store data relative to the face

    """

    @classmethod
    def from_face(cls, face):
        return cls(
            face.points,
            face.uuid,
            face.data
        )


class Cell(Element):
    """ Cell element

    Element for storing 3D geometrical objects

    Parameters
    ----------
    uuid :
        uuid of the cell.
    points: list of Point
        list of points defining the cell.
    data: DataContainer
        object to store data relative to the cell

    """

    @classmethod
    def from_cell(cls, cell):
        return cls(
            cell.points,
            cell.uuid,
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

    Attributes
    ----------
    data : Data
        The X coordinate.
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

    def __init__(self):
        self.data = 0

        self._points = {}
        self._edges = {}
        self._faces = {}
        self._cells = {}

    def get_point(self, uuid):
        """ Returns a point with a given uuid.

        Returns the point stored in the mesh
        identified by uuid. If such point do not
        exists an exception is raised.

        Parameters
        ----------
        uuid
            uuid of the desired point.

        Returns
        -------
        Point
            Mesh point identified by uuid

        Raises
        ------
        Exception
            If the point identified by uuid was not found

        """

        try:
            return Point.from_point(self._points[uuid])
        except KeyError:
            error_str = "Trying to get an non-existing point with uuid: {}"
            raise ValueError(error_str.format(uuid))

    def get_edge(self, uuid):
        """ Returns an edge with a given uuid.

        Returns the edge stored in the mesh
        identified by uuid. If such edge do not
        exists an exception is raised.

        Parameters
        ----------
        uuid
            uuid of the desired edge.

        Returns
        -------
        Edge
            Edge identified by uuid

        Raises
        ------
        Exception
            If the edge identified by uuid was not found

        """

        try:
            return Edge.from_edge(self._edges[uuid])
        except KeyError:
            error_str = "Trying to get an non-existing edge with uuid: {}"
            raise ValueError(error_str.format(uuid))

    def get_face(self, uuid):
        """ Returns a face with a given uuid.

        Returns the face stored in the mesh
        identified by uuid. If such face do not
        exists an exception is raised.

        Parameters
        ----------
        uuid
            uuid of the desired face.

        Returns
        -------
        Face
            Face identified by uuid

        Raises
        ------
        Exception
            If the face identified by uuid was not found

        """

        try:
            return Face.from_face(self._faces[uuid])
        except KeyError:
            error_str = "Trying to get an non-existing face with uuid: {}"
            raise ValueError(error_str.format(uuid))

    def get_cell(self, uuid):
        """ Returns a cell with a given uuid.

        Returns the cell stored in the mesh
        identified by uuid . If such cell do not
        exists an exception is raised.

        Parameters
        ----------
        uuid
            uuid of the desired cell.

        Returns
        -------
        Cell
            Cell with id identified by uuid

        Raises
        ------
        Exception
            If the cell identified by uuid was not found

        """

        try:
            return Cell.from_cell(self._cells[uuid])
        except KeyError:
            error_str = "Trying to get an non-existing cell with uuid: {}"
            raise ValueError(error_str.format(uuid))

    def add_point(self, point):
        """ Adds a new point to the mesh.

        Parameters
        ----------
        point : Point
            Point to be added to the mesh

        Raises
        ------
        KeyError
            If other point with the same uuid was already
            in the mesh

        TypeError
            If the object provided is not a point

        """

        if point.uuid is None:
            point.uuid = self._generate_uuid()

        if point.uuid in self._points:
            error_str = "Trying to add an already existing point with uuid: "\
                + str(point.uuid)
            raise KeyError(error_str)

        self._points[point.uuid] = Point.from_point(point)

        return point.uuid

    def add_edge(self, edge):
        """ Adds a new edge to the mesh.

        Parameters
        ----------
        edge : Edge
            Edge to be added to the mesh

        Raises
        ------
        KeyError
            If other edge with the same uuid was already
            in the mesh

        TypeError
            If the object provided is not an edge

        """

        if edge.uuid is None:
            edge.uuid = self._generate_uuid()

        if edge.uuid in self._edges:
            error_str = "Trying to add an already existing edge with uuid: "\
                + str(edge.uuid)
            raise KeyError(error_str)

        self._edges[edge.uuid] = Edge.from_edge(edge)

        return edge.uuid

    def add_face(self, face):
        """ Adds a new face to the mesh.

        Parameters
        ----------
        face : Face
            Face to be added to the mesh

        Raises
        ------
        KeyError
            If other face with the same uuid was already
            in the mesh

        TypeError
            If the object provided is not a face

        """

        if face.uuid is None:
            face.uuid = self._generate_uuid()

        if face.uuid in self._faces:
            error_str = "Trying to add an already existing face with uuid: "\
                + str(face.uuid)
            raise KeyError(error_str)

        self._faces[face.uuid] = Face.from_face(face)

        return face.uuid

    def add_cell(self, cell):
        """ Adds a new cell to the mesh.

        Parameters
        ----------
        cell : Cell
            Cell to be added to the mesh

        Raises
        ------
        KeyError
            If other cell with the same uuid was already
            in the mesh

        TypeError
            If the object provided is not a cell

        """

        if cell.uuid is None:
            cell.uuid = self._generate_uuid()

        if cell.uuid in self._cells:
            error_str = "Trying to add an already existing cell with uuid: "\
                + str(cell.uuid)
            raise KeyError(error_str)

        self._cells[cell.uuid] = Cell.from_cell(cell)

        return cell.uuid

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

        TypeError
            If the object provided is not a point

        """

        if point.uuid not in self._points:
            error_str = "Trying to update a non-existing point with uuid: "\
                + str(point.uuid)
            raise KeyError(error_str)

        if not isinstance(point, Point):
            error_str = "Trying to update an object with the wrong type. "\
                + "Point expected."
            raise TypeError(error_str)

        point_to_update = self._points[point.uuid]

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

        TypeError
            If the object provided is not an edge

        """

        if edge.uuid not in self._edges:
            error_str = "Trying to update a non-existing edge with uuid: "\
                + str(edge.uuid)
            raise KeyError(error_str)

        if not isinstance(edge, Edge):
            error_str = "Trying to update an object with the wrong type. "\
                + "Edge expected."
            raise TypeError(error_str)

        edge_to_update = self._edges[edge.uuid]

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

        TypeError
            If the object provided is not a face

        """

        if face.uuid not in self._faces:
            error_str = "Trying to update a non-existing face with uuid: "\
                + str(face.uuid)
            raise KeyError(error_str)

        if not isinstance(face, Face):
            error_str = "Trying to update an object with the wrong type. "\
                + "Face expected."
            raise TypeError(error_str)

        face_to_update = self._faces[face.uuid]

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
        KeyError
            If the cell was not found in the mesh

        TypeError
            If the object provided is not a cell

        """

        if cell.uuid not in self._cells:
            error_str = "Trying to update a non-existing cell with uuid: "\
                + str(cell.uuid)
            raise KeyError(error_str)

        if not isinstance(cell, Cell):
            error_str = "Trying to update an object with the wrong type. "\
                + "Cell expected."
            raise TypeError(error_str)

        cell_to_update = self._cells[cell.uuid]

        cell_to_update.data = cell.data
        cell_to_update.points = cell.points

    def iter_points(self, point_uuids=None):
        """ Returns an iterator over the selected points.

        Returns an iterator over the points with uuid in
        point_ids. If none of the ids in point_ids exists,
        an empty iterator is returned. If there is no ids
        inside point_ids, a iterator over all points of
        the mesh is returned instead.

        Parameters
        ----------
        point_uuids : list of uuids, optional
            uuids of the desired points, default empty

        Returns
        -------
        iter
            Iterator over the selected points

        """

        if point_uuids is None:
            for point in self._points.values():
                yield Point.from_point(point)
        else:
            for point_uuid in point_uuids:
                yield Point.from_point(self._points[point_uuid])

    def iter_edges(self, edge_uuids=None):
        """ Returns an iterator over the selected edges.

        Returns an iterator over the edged with uuid in
        edge_uuid. If none of the uuids in edge_uuids exists,
        an empty iterator is returned. If there is no uuids
        inside edge_uuids, a iterator over all edges of
        the mesh is returned instead.

        Parameters
        ----------
        edge_uuids : list of uuids, optional
            Uuids of the desired edges, default empty

        Returns
        -------
        iter
            Iterator over the selected edges

        """

        if edge_uuids is None:
            for edge in self._edges.values():
                yield Edge.from_edge(edge)
        else:
            for edge_uuid in edge_uuids:
                yield Edge.from_edge(self._edges[edge_uuid])

    def iter_faces(self, face_uuids=None):
        """ Returns an iterator over the selected faces.

        Returns an iterator over the faces with uuid in
        face_uuids. If none of the uuids in face_uuids exists,
        an empty iterator is returned. If there is no uuids
        inside face_uuids, a iterator over all faces of
        the mesh is returned instead.

        Parameters
        ----------
        face_uuids : list of uuids, optional
            Uuids of the desired faces, default empty

        Returns
        -------
        iter
            Iterator over the selected faces

        """

        if face_uuids is None:
            for face in self._faces.values():
                yield Face.from_face(face)
        else:
            for face_uuid in face_uuids:
                yield Face.from_face(self._faces[face_uuid])

    def iter_cells(self, cell_uuids=None):
        """ Returns an iterator over the selected cells.

        Returns an iterator over the cells with uuid in
        cell_uuids. If none of the uuids in cell_uuids exists,
        an empty iterator is returned. If there is no uuids
        inside cell_uuids, a iterator over all cells of
        the mesh is returned instead.

        Parameters
        ----------
        cell_uuids : list of uuids, optional
            Uuids of the desired cell, default empty

        Returns
        -------
        iter
            Iterator over the selected cells

        """

        if cell_uuids is None:
            for cell in self._cells.values():
                yield Cell.from_cell(cell)
        else:
            for cell_uuid in cell_uuids:
                yield Cell.from_cell(self._cells[cell_uuid])

    def has_edges(self):
        """ Check if the mesh has edges

        Returns
        -------
        bool
            True of there are edges inside the mesh,
            False otherwise

        """

        return len(self._edges) > 0

    def has_faces(self):
        """ Check if the mesh has faces

        Returns
        -------
        bool
            True of there are faces inside the mesh,
            False otherwise

        """
        return len(self._faces) > 0

    def has_cells(self):
        """ Check if the mesh has cells

        Returns
        -------
        bool
            True of there are cells inside the mesh,
            False otherwise

        """
        return len(self._cells) > 0

    def _generate_uuid(self):
        """ Provides and uuid for the object

        Provides san uuid as defined in the standard RFC 4122
        """

        return uuid.uuid4()
