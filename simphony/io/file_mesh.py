""" Mesh File

This module contains the implentation to store, acces,
and modify a file storing mesh data

"""
import tables
import uuid
import simphony.core.data_container as dc

from simphony.cuds.abstractmesh import ABCMesh
from simphony.cuds.mesh import Mesh
from simphony.cuds.mesh import Point
from simphony.cuds.mesh import Edge
from simphony.cuds.mesh import Face
from simphony.cuds.mesh import Cell

MAX_POINTS_IN_EDGE = 2
MAX_POINTS_IN_FACE = 3
MAX_POINTS_IN_CELL = 4

class _PointDescriptor(tables.IsDescription):
    """ Descriptor for storing Point information

    Provides the column definition to store Point
    information (x, y, z).

    """

    uuid = tables.StringCol(32,pos=1)
    coordinates = tables.Float64Col(
        pos=2, shape=(3,)
        )

# Note: Should length,area and volumne be saved here?
class _EdgeDescriptor(tables.IsDescription):
    """ Descriptor for storing Edge information

    Provides the column definition to store Points
    forming an edge and its data.

    """

    uuid = tables.StringCol(32,pos=1)
    points_uuids = tables.StringCol(
        32, pos=2, shape=(MAX_POINTS_IN_EDGE,)
        )

class _FaceDescriptor(tables.IsDescription):
    """ Descriptor for storing Face information

    Provides the column definition to store Points
    forming a face and its data.

    """

    uuid = tables.StringCol(32,pos=1)
    points_uuids = tables.StringCol(
        32, pos=2, shape=(MAX_POINTS_IN_FACE,)
        )

class _CellDescriptor(tables.IsDescription):
    """ Descriptor for storing Cell information

    Provides the column definition to store Points
    forming a cell and its data.

    """

    uuid = tables.StringCol(32,pos=1)
    points_uuids = tables.StringCol(
        32, pos=2, shape=(MAX_POINTS_IN_CELL,)
        )

class _MeshDescriptor(tables.IsDescription):
    """ Descriptor for storing Mesh information

    Provides the column definition to store mesh data.

    """

    uuid = tables.StringCol(32,pos=1)

class FileMesh(object):
    """ FileMesh.

    Interface of the mesh file driver.
    Stores general mesh information Points and Elements
    such as Edges, Faces and Cells and provide the
    methods to interact with them. The methods are
    divided in four diferent blocks:

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

    def __init__(self, group, meshFile):
        self._file = meshFile
        self._group = group

        if "points" not in self._group:
            self._create_points_table()

        if "edges" not in self._group:
            self._create_edges_table()

        if "faces" not in self._group:
            self._create_faces_table()

        if "cells" not in self._group:
            self._create_cells_table()

    def get_point(self, p_uuid):
        """ Returns a point with a given uuid.

        Returns the point stored in the mesh
        identified by uuid. If such point do not
        exists an exception is raised.

        Parameters
        ----------
        uuid : int
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
            for row in self._group.points:
                if row['uuid'] == p_uuid.bytes:
                    return Point(
                        tuple(row['coordinates']),
                        uuid.UUID(bytes=row['uuid'])
                        )
        except KeyError:
            error_str = "Trying to get an non existing point with uuid: {}"
            raise ValueError(error_str.format(p_uuid))

    def get_edge(self, e_uuid):
        """ Returns an edge with a given uuid.

        Returns the edge stored in the mesh
        identified by uuid. If such edge do not
        exists a exception is raised.

        Parameters
        ----------
        uuid : uint64
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
            for row in self._group.edges:
                if row['uuid'] == e_uuid.bytes:
                    return Edge(
                        list(uuid.UUID(bytes=pb) for pb in row['points_uuids']),
                        uuid.UUID(bytes=row['uuid'])
                        )
        except:
            error_str = "Trying to get an non existing edge with uuid: {}"
            raise ValueError(error_str.format(e_uuid))

    def get_face(self, f_uuid):
        """ Returns an face with a given uuid.

        Returns the face stored in the mesh
        identified by uuid. If such face do not
        exists a exception is raised.

        Parameters
        ----------
        uuid : uint64
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
            for row in self._group.faces:
                if row['uuid'] == f_uuid.bytes:
                    return Face(
                        list(uuid.UUID(bytes=pb) for pb in row['points_uuids']),
                        uuid.UUID(bytes=row['uuid'])
                        )
        except:
            error_str = "Trying to get an non existing face with uuid: {}"
            raise ValueError(error_str.format(f_uuid))

    def get_cell(self, c_uuid):
        """ Returns an cell with a given uuid.

        Returns the cell stored in the mesh
        identified by uuid . If such cell do not
        exists a exception is raised.

        Parameters
        ----------
        uuid : uint64
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
            for row in self._group.cells:
                if row['uuid'] == c_uuid.bytes:
                    return Cell(
                        list(uuid.UUID(bytes=pb) for pb in row['points_uuids']),
                        uuid.UUID(bytes=row['uuid'])
                        )
        except:
            error_str = "Trying to get an non existing cell with id: {}"
            raise ValueError(error_str.format(c_uuid))

    def add_point(self, point):
        """ Adds a new point to the mesh container.

        Parameters
        ----------
        point : Point
            Point to be added to the mesh container

        Raises
        ------
        KeyError
            If other point with the same uuid was already
            in the mesh

        """

        if point.uuid is None:
            point.uuid = self._generate_uuid()

        for row in self._group.points:
            if row['uuid'] == point.uuid.bytes:
                error_str = "Trying to add an already existing point with uuid: "\
                    + str(point.uuid)
                raise KeyError(error_str)

        row = self._group.points.row;

        row['uuid'] = point.uuid.bytes
        row['coordinates'] = point.coordinates

        row.append()
        self._group.points.flush()

        return point.uuid

    def add_edge(self, edge):
        """ Adds a new edge to the mesh container.

        Parameters
        ----------
        edge : Edge
            Edge to be added to the mesh container

        Raises
        ------
        KeyError
            If other edge with the same uuid was already
            in the mesh

        """

        if edge.uuid is None:
            edge.uuid = self._generate_uuid()

        for row in self._group.edges:
            if row['uuid'] == edge.uuid.bytes:
                error_str = "Trying to add an already existing edge with uuid: "\
                    + str(edge.uuid)
                raise KeyError(error_str)

        row = self._group.edges.row;

        row['uuid'] = edge.uuid.bytes
        row['points_uuids'] = [puuid.bytes for puuid in edge.points]

        row.append()
        self._group.edges.flush()

        return edge.uuid

    def add_face(self, face):
        """ Adds a new face to the mesh container.

        Parameters
        ----------
        face : Face
            Face to be added to the mesh container

        Raises
        ------
        KeyError
            If other face with the same uuid was already
            in the mesh

        """

        if face.uuid is None:
            face.uuid = self._generate_uuid()

        for row in self._group.faces:
            if row['uuid'] == face.uuid.bytes:
                error_str = "Trying to add an already existing face with uuid: "\
                    + str(face.uuid)
                raise KeyError(error_str)

        row = self._group.faces.row;

        row['uuid'] = face.uuid.bytes
        row['points_uuids'] = [puuid.bytes for puuid in face.points]

        row.append()
        self._group.faces.flush()

        return face.uuid

    def add_cell(self, cell):
        """ Adds a new cell to the mesh container.

        Parameters
        ----------
        cell : Cell
            Cell to be added to the mesh container

        Raises
        ------
        KeyError
            If other cell with the same uuid was already
            in the mesh

        """

        if cell.uuid is None:
            cell.uuid = self._generate_uuid()

        for row in self._group.cells:
            if row['uuid'] == cell.uuid.bytes:
                error_str = "Trying to add an already existing cell with uuid: "\
                    + str(cell.uuid)
                raise KeyError(error_str)

        row = self._group.cells.row;

        row['uuid'] = cell.uuid.bytes
        row['points_uuids'] = [puuid.bytes for puuid in cell.points]

        row.append()
        self._group.cells.flush()

        return cell.uuid

    def update_point(self, point):
        """ Updates the information of a point.

        Gets the mesh point identified by the same
        id as the provided point and updates its information.

        Parameters
        ----------
        point : Point
            Point to be updated

        Raises
        ------
        KeyError
            If the point was not found in the mesh container.

        """

        for row in self._group.points:
            if row['uuid'] == point.uuid.bytes:
                row['coordinates'] = list(point.coordinates)
                row.update()
                row._flush_mod_rows()
            else:
                error_str = "Trying to add an already existing point with uuid: "\
                    + str(point.uuid)
                raise KeyError(error_str)

    def update_edge(self, edge):
        """ Updates the information of an edge.

        Gets the mesh edge identified by the same
        id as the provided edge and updates its information.

        Parameters
        ----------
        edge : Edge
            Edge to be updated.

        Raises
        ------
        KeyError
            If the edge was not found in the mesh container.

        """

        for row in self._group.edges:
            if row['uuid'] == edge.uuid.bytes:
                row['points_uuids'] = [puuid.bytes for puuid in edge.points]
                row.update()
                row._flush_mod_rows()
            else:
                error_str = "Trying to add an already existing edge with uuid: "\
                    + str(edge.uuid)
                raise KeyError(error_str)

    def update_face(self, face):
        """ Updates the information of a face.

        Gets the mesh face identified by the same
        id as the provided face and updates its information.

        Parameters
        ----------
        face : Face
            Face to be updated.

        Raises
        ------
        KeyError
            If the face was not found in the mesh container.

        """

        for row in self._group.faces:
            if row['uuid'] == face.uuid.bytes:
                row['points_uuids'] = [puuid.bytes for puuid in face.points]
                row.update()
                row._flush_mod_rows()
            else:
                error_str = "Trying to add an already existing face with uuid: "\
                    + str(face.uuid)
                raise KeyError(error_str)

    def update_cell(self, cell):
        """ Updates the information of a cell.

        Gets the mesh cell identified by the same
        id as the provided cell and updates its information.

        Parameters
        ----------
        cell : Cell
            Cell to be updated.

        Raises
        ------
        KeyError
            If the cell was not found in the mesh container.

        """

        for row in self._group.cells:
            if row['uuid'] == cell.uuid.bytes:
                row['points_uuids'] = [puuid.bytes for puuid in cell.points]
                row.update()
                row._flush_mod_rows()
            else:
                error_str = "Trying to add an already existing cell with uuid: "\
                    + str(cell.uuid)
                raise KeyError(error_str)

    def iter_points(self, point_uuids=None):
        """ Returns an iterator over the selected points.

        Returns an interator over the points with id in
        point_ids. If non of the ids in point_ids exists,
        an empty iterator is returned. If there is no ids
        inside point_ids, a iterator over all points of
        the mesh is returned insted.

        Parameters
        ----------
        point_uuids : list of uint64, optional
            Uuids of the desired points, default empty

        Returns
        -------
        iter
            Iterator over the selected points

        """

        if point_uuids is None:
            for row in self._group.points:
                yield Point(
                    tuple(row['coordinates']),
                    uuid.UUID(bytes=row['uuid'])
                )
        else:
            for point_uuid in point_uuids:
                yield self.get_point(point_uuid)

    def iter_edges(self, edge_uuids=None):
        """ Returns an iterator over the selected edges.

        Returns an interator over the edged with id in
        edge_id. If non of the ids in edge_ids exists,
        an empty iterator is returned. If there is no ids
        inside edge_ids, a iterator over all edges of
        the mesh is returned insted.

        Parameters
        ----------
        edge_uuids : list of uint64, optional
            Uuids of the desired edges, default empty

        Returns
        -------
        iter
            Iterator over the selected edges

        """

        if edge_uuids is None:
            for row in self._group.edges:
                yield Edge(
                    list(row['points_uuids']),
                    uuid.UUID(bytes=row['uuid'])
                )
        else:
            for edge_uuid in edge_uuids:
                yield self.get_edge(edge_uuid)

    def iter_faces(self, face_uuids=None):
        """ Returns an iterator over the selected faces.

        Returns an interator over the faces with id in
        face_ids. If non of the ids in face_ids exists,
        an empty iterator is returned. If there is no ids
        inside face_ids, a iterator over all faces of
        the mesh is returned insted.

        Parameters
        ----------
        face_uuids : list of uint64, optional
            Uuids of the desired faces, default empty

        Returns
        -------
        iter
            Iterator over the selected faces

        """

        if face_uuids is None:
            for row in self._group.faces:
                yield Face(
                    list(row['points_uuids']),
                    uuid.UUID(bytes=row['uuid'])
                )
        else:
            for face_uuid in face_uuids:
                yield self.get_face(face_uuid)

    def iter_cells(self, cell_uuids=None):
        """ Returns an iterator over the selected cells.

        Returns an interator over the cells with id in
        cell_ids. If non of the ids in cell_ids exists,
        an empty iterator is returned. If there is no ids
        inside cell_ids, a iterator over all cells of
        the mesh is returned insted.

        Parameters
        ----------
        cell_uuids : list of uint64, optional
            Uuids of the desired cell, default empty

        Returns
        -------
        iter
            Iterator over the selected cells

        """

        if cell_uuids is None:
            for row in self._group.cells:
                yield Cell(
                    list(row['points_uuids']),
                    uuid.UUID(bytes=row['uuid'])
                )
        else:
            for cell_uuid in cell_uuids:
                yield self.get_cell(cell_uuid)

    def has_edges(self):
        """ Check if the mesh container has edges

        Returns
        -------
        bool
            True of there are edges inside the mesh,
            False otherwise

        """

        return self._group.edges.nrows != 0

    def has_faces(self):
        """ Check if the mesh container has faces

        Returns
        -------
        bool
            True of there are faces inside the mesh,
            False otherwise

        """
        return self._group.faces.nrows != 0

    def has_cells(self):
        """ Check if the mesh container has cells

        Returns
        -------
        bool
            True of there are cells inside the mesh,
            False otherwise

        """
        return self._group.cells.nrows != 0

    def _generate_uuid(self):
        """ Provides and id for the object

        Provides an uuid as defined in the standard RFC 4122
        """

        return uuid.uuid4()

    def _create_points_table(self):
            self._file.create_table(
                self._group, "points", _PointDescriptor)

    def _create_edges_table(self):
            self._file.create_table(
                self._group, "edges", _EdgeDescriptor)

    def _create_faces_table(self):
            self._file.create_table(
                self._group, "faces", _FaceDescriptor)

    def _create_cells_table(self):
            self._file.create_table(
                self._group, "cells", _CellDescriptor)