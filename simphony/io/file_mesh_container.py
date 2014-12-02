""" Mesh File

This module contains the implentation to store, acces,
and modify a file storing mesh data

"""
import tables
import uuid
import copy

from simphony.cuds.abstractmesh import ABCMesh
from simphony.cuds.mesh import Mesh, Edge, Face, Cell

MAX_POINTS_IN_EDGE = 2
MAX_POINTS_IN_FACE = 3
MAX_POINTS_IN_CELL = 4

class _PointDescriptor(tables.IsDescription):
    """ Descriptor for storing Point information

    Provides the column definition to store Point
    information (x, y, z).

    """

    uuid = tables.Float128Col(pos=1)
    coordinates = tables.Float64Col(
        pos=2, shape=(3,)
        )

# Note: Should length,area and volumne be saved here?
class _EdgeDescriptor(tables.IsDescription):
    """ Descriptor for storing Edge information

    Provides the column definition to store Points
    forming an edge and its data.

    """

    uuid = tables.Float128Col(pos=1)
    points_ids = tables.Float64Col(
        pos=2, shape=(POINTS_IN_EDGE,)
        )

class _FaceDescriptor(tables.IsDescription):
    """ Descriptor for storing Face information

    Provides the column definition to store Points
    forming a face and its data.

    """

    uuid = tables.Float128Col(pos=1)
    points_ids = tables.Float64Col(
        pos=2, shape=(POINTS_IN_FACE,)
        )

class _CellDescriptor(tables.IsDescription):
    """ Descriptor for storing Cell information

    Provides the column definition to store Points
    forming a cell and its data.

    """

    uuid = tables.Float128Col(pos=1)
    points_ids = tables.Float64Col(
        pos=2, shape=(POINTS_IN_CELL,)
        )

class _MeshDescriptor(tables.IsDescription):
    """ Descriptor for storing Mesh information

    Provides the column definition to store mesh data.

    """

    uuid = tables.Float128Col(pos=1)
    edges_ids = tables.Float64Col(pos=2)
    faces_ids = tables.Float64Col(pos=3)
    cells_ids = tables.Float64Col(pos=4)

class FileMeshContainer(object):

    def __init__(self, grpup, meshFile):
        self._file = meshFile
        self._group = group

        if "points" not in self._group
            self._create_points_table()

        if "edges" not in self._group
            self._create_edges_table()

        if "faces" not in self._group
            self._create_faces_table()

        if "cells" not in self._group
            self._create_cells_table()

    def get_point(self, uuid):
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
        NotFoundException
            If the point identified by uuid was not found

        """

        for row in self._group.points.where(
            "id == value", condvars={"value": uuid}
            ):
            return Point(
                row['id'],
                tuple(row['coordinates']),
                None
                None
                )
        else:
            error_str = "Trying to get an non existing point with uuid: "\
                + str(point.id)
            raise KeyError(error_str)

    def get_edge(self, uuid):
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
        NotFoundException
            If the edge identified by uuid was not found

        """

        for row in self._group.edges.where(
            "id == value", condvars={"value": uuid}
            ):
            return Edge(
                row['id'],
                list(row['points_ids']),
                None
                None
                )
        else:
            error_str = "Trying to get an non existing edge with uuid: "\
                + str(uuid)
            raise Exception(error_str)

    def get_face(self, uuid):
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
        NotFoundException
            If the face identified by uuid was not found

        """

        for row in self._group.faces.where(
            "id == value", condvars={"value": uuid}
            ):
            return Face(
                row['id'],
                list(row['points_ids']),
                None
                None
                )
        else:
            error_str = "Trying to get an non existing face with uuid: "\
                + str(uuid)
            raise Exception(error_str)

    def get_cell(self, uuid):
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
        NotFoundException
            If the cell identified by uuid was not found

        """

        for row in self._group.cells.where(
            "id == value", condvars={"value": uuid}
            ):
            return Cell(
                row['id'],
                list(row['points_ids']),
                None
                None
                )
        else:
            error_str = "Trying to get an non existing cell with id: "\
                + str(uuid)
            raise Exception(error_str)

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

        if point.id is None:
            point.id = self._generate_uuid()

        for _ in self._group.points.where(
            "id == value", condvars={"value": point.id}
            ):
            error_str = "Trying to add an already existing point with uuid: "\
                + str(point.id)
            raise KeyError(error_str)

        self._group.points.append([
            point.id,
            point.coordinates
            ])

        return point.id

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

        if edge.id is None:
            edge.id = self._generate_uuid()

        for _ in self._group.edges.where(
            "id == value", condvars={"value": edge.id}
            ):
            error_str = "Trying to add an already existing edge with uuid: "\
                + str(edge.id)
            raise KeyError(error_str)

        self._group.edges.append([
            edge.id,
            edge.points
            ])

        return edge.id

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

        if face.id is None:
            face.id = self._generate_uuid()

        for _ in self._group.faces.where(
            "id == value", condvars={"value": face.id}
            ):
            error_str = "Trying to add an already existing face with uuid: "\
                + str(face.id)
            raise KeyError(error_str)

        self._group.faces.append([
            face.id,
            face.points
            ])

        return face.id

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

        if cell.id is None:
            cell.id = self._generate_uuid()

        for _ in self._group.cells.where(
            "id == value", condvars={"value": cell.id}
            ):
            error_str = "Trying to add an already existing cell with uuid: "\
                + str(cell.id)
            raise KeyError(error_str)

        self._group.cells.append([
            cell.id,
            cell.points
            ])

        return cell.id

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

        for row in self._group.points.where(
            "id == value", condvars={"value": point.id}
            ):
            row['coordinates'] = list(point.coordinates)
            row.update()
            row._flush_mod_rows()
        else:
            error_str = "Trying to add an already existing point with uuid: "\
                + str(point.id)
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

        for row in self._group.edges.where(
            "id == value", condvars={"value": edge.id}
            ):
            row['points_ids'] = list(edge.points)
            row.update()
            row._flush_mod_rows()
        else:
            error_str = "Trying to add an already existing edge with uuid: "\
                + str(edge.id)
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

        for row in self._group.faces.where(
            "id == value", condvars={"value": face.id}
            ):
            row['points_ids'] = list(face.points)
            row.update()
            row._flush_mod_rows()
        else:
            error_str = "Trying to add an already existing face with uuid: "\
                + str(face.id)
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

        for row in self._group.cells.where(
            "id == value", condvars={"value": cell.id}
            ):
            row['points_ids'] = list(cell.points)
            row.update()
            row._flush_mod_rows()
        else:
            error_str = "Trying to add an already existing cell with uuid: "\
                + str(cell.id)
            raise KeyError(error_str)

    def iter_points(self, point_ids=None):
        """ Returns an iterator over the selected points.

        Returns an interator over the points with id in
        point_ids. If non of the ids in point_ids exists,
        an empty iterator is returned. If there is no ids
        inside point_ids, a iterator over all points of
        the mesh is returned insted.

        Parameters
        ----------
        point_ids : list of uint64, optional
            Uuids of the desired points, default empty

        Returns
        -------
        iter
            Iterator over the selected points

        """

        if point_ids is None:
            for row in self._group.edges:
                yield Edge(
                    row['id'],
                    tuple(row['coordinates']),
                    None
                    None
                )
        else:
            for point_id in point_ids:
                yield self.get_point(point_id)

    def iter_edges(self, edge_ids=None):
        """ Returns an iterator over the selected edges.

        Returns an interator over the edged with id in
        edge_id. If non of the ids in edge_ids exists,
        an empty iterator is returned. If there is no ids
        inside edge_ids, a iterator over all edges of
        the mesh is returned insted.

        Parameters
        ----------
        edge_ids : list of uint64, optional
            Uuids of the desired edges, default empty

        Returns
        -------
        iter
            Iterator over the selected edges

        """

        if edge_ids is None:
            for row in self._group.edges:
                yield Edge(
                    row['id'],
                    list(row['points_ids']),
                    None
                    None
                )
        else:
            for edge_id in edge_ids:
                yield self.get_edge(edge_id)

    def iter_faces(self, face_ids=None):
        """ Returns an iterator over the selected faces.

        Returns an interator over the faces with id in
        face_ids. If non of the ids in face_ids exists,
        an empty iterator is returned. If there is no ids
        inside face_ids, a iterator over all faces of
        the mesh is returned insted.

        Parameters
        ----------
        face_ids : list of uint64, optional
            Uuids of the desired faces, default empty

        Returns
        -------
        iter
            Iterator over the selected faces

        """

        if face_ids is None:
            for row in self._group.faces:
                yield Face(
                    row['id'],
                    list(row['points_ids']),
                    None
                    None
                )
        else:
            for face_id in face_ids:
                yield self.get_face(face_id)

    def iter_cells(self, cell_ids=None):
        """ Returns an iterator over the selected cells.

        Returns an interator over the cells with id in
        cell_ids. If non of the ids in cell_ids exists,
        an empty iterator is returned. If there is no ids
        inside cell_ids, a iterator over all cells of
        the mesh is returned insted.

        Parameters
        ----------
        cell_ids : list of uint64, optional
            Uuids of the desired cell, default empty

        Returns
        -------
        iter
            Iterator over the selected cells

        """

        if cell_ids is None:
            for row in self._group.cells:
                yield Cell(
                    row['id'],
                    list(row['points_ids']),
                    None
                    None
                )
        else:
            for cell_id in cell_ids:
                yield self.get_cell(cell_id)

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

        return uuid.uuid1()