""" Mesh File

This module contains the implentation to store, acces,
and modify a file storing mesh data

"""
import tables
import uuid

from simphony.cuds.mesh import Point
from simphony.cuds.mesh import Edge
from simphony.cuds.mesh import Face
from simphony.cuds.mesh import Cell

from simphony.io.data_container_table import DataContainerTable

MAX_POINTS_IN_EDGE = 2
MAX_POINTS_IN_FACE = 4
MAX_POINTS_IN_CELL = 8


class _PointDescriptor(tables.IsDescription):
    """ Descriptor for storing Point information

    Provides the column definition to store Point
    information (x, y, z).

    """

    uid = tables.StringCol(32, pos=0)
    data = tables.StringCol(32, pos=1)
    coordinates = tables.Float64Col(
        pos=2, shape=(3,)
        )


class _EdgeDescriptor(tables.IsDescription):
    """ Descriptor for storing Edge information

    Provides the column definition to store Edges
    forming an edge and its data.

    """

    uid = tables.StringCol(32, pos=0)
    data = tables.StringCol(32, pos=1)
    points_uids = tables.StringCol(
        32, pos=2, shape=(MAX_POINTS_IN_EDGE,)
        )
    n_points = tables.UInt32Col(pos=3)


class _FaceDescriptor(tables.IsDescription):
    """ Descriptor for storing Face information

    Provides the column definition to store Faces
    forming a face and its data.

    """

    uid = tables.StringCol(32, pos=0)
    data = tables.StringCol(32, pos=1)
    points_uids = tables.StringCol(
        32, pos=2, shape=(MAX_POINTS_IN_FACE,)
        )
    n_points = tables.UInt32Col(pos=3)


class _CellDescriptor(tables.IsDescription):
    """ Descriptor for storing Cell information

    Provides the column definition to store Cells
    forming a cell and its data.

    """

    uid = tables.StringCol(32, pos=0)
    data = tables.StringCol(32, pos=1)
    points_uids = tables.StringCol(
        32, pos=2, shape=(MAX_POINTS_IN_CELL,)
        )
    n_points = tables.UInt32Col(pos=3)


class FileMesh(object):
    """ FileMesh.

    Interface of the mesh file driver.
    Stores general mesh information Points and Elements
    such as Edges, Faces and Cells and provide the
    methods to interact with them. The methods are
    divided in four diferent blocks:

    (1) methods to get the related item with the provided uid;
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
    _create_points_table, _create_edges_table
    _create_faces_table, _create_cells_table

    """

    def __init__(self, group, meshFile):

        self._file = meshFile
        self._group = group
        self._create_data_table()

        if "points" not in self._group:
            self._create_points_table()

        if "edges" not in self._group:
            self._create_edges_table()

        if "faces" not in self._group:
            self._create_faces_table()

        if "cells" not in self._group:
            self._create_cells_table()

    def get_point(self, p_uid):
        """ Returns a point with a given uid.

        Returns the point stored in the mesh
        identified by uid. If such point do not
        exists an exception is raised.

        Parameters
        ----------
        uid : int
            uid of the desired point.

        Returns
        -------
        Point
            Mesh point identified by uid

        Raises
        ------
        Exception
            If the point identified by uid was not found

        """

        for row in self._group.points.where(
                'uid == value', condvars={'value': p_uid.hex}):
            return Point(
                tuple(row['coordinates']),
                uuid.UUID(hex=row['uid'], version=4),
                self._data[uuid.UUID(hex=row['data'], version=4)]
                )
        else:
            error_str = "Trying to get an non existing point with uid: {}"
            raise ValueError(error_str.format(p_uid))

    def get_edge(self, e_uid):
        """ Returns an edge with a given uid.

        Returns the edge stored in the mesh
        identified by uid. If such edge do not
        exists a exception is raised.

        Parameters
        ----------
        uid : uint64
            uid of the desired edge.

        Returns
        -------
        Edge
            Edge identified by uid

        Raises
        ------
        Exception
            If the edge identified by uid was not found

        """

        for row in self._group.edges.where(
                'uid == value', condvars={'value': e_uid.hex}):
            return Edge(
                list(uuid.UUID(hex=pb) for pb in
                     row['points_uids'][0:row['n_points']]),
                uuid.UUID(hex=row['uid'], version=4),
                self._data[uuid.UUID(hex=row['data'], version=4)]
                )
        else:
            error_str = "Trying to get an non existing edge with uid: {}"
            raise ValueError(error_str.format(e_uid))

    def get_face(self, f_uid):
        """ Returns an face with a given uid.

        Returns the face stored in the mesh
        identified by uid. If such face do not
        exists a exception is raised.

        Parameters
        ----------
        uid : uint64
            uid of the desired face.

        Returns
        -------
        Face
            Face identified by uid

        Raises
        ------
        Exception
            If the face identified by uid was not found

        """

        for row in self._group.faces.where(
                'uid == value', condvars={'value': f_uid.hex}):
            return Face(
                list(uuid.UUID(hex=pb, version=4) for pb in
                     row['points_uids'][0:row['n_points']]),
                uuid.UUID(hex=row['uid'], version=4),
                self._data[uuid.UUID(hex=row['data'], version=4)]
                )
        else:
            error_str = "Trying to get an non existing face with uid: {}"
            raise ValueError(error_str.format(f_uid))

    def get_cell(self, c_uid):
        """ Returns an cell with a given uid.

        Returns the cell stored in the mesh
        identified by uid . If such cell do not
        exists a exception is raised.

        Parameters
        ----------
        uid : uint64
            uid of the desired cell.

        Returns
        -------
        Cell
            Cell with id identified by uid

        Raises
        ------
        Exception
            If the cell identified by uid was not found

        """

        for row in self._group.cells.where(
                'uid == value', condvars={'value': c_uid.hex}):
            return Cell(
                list(uuid.UUID(hex=pb, version=4) for pb in
                     row['points_uids'][0:row['n_points']]),
                uuid.UUID(hex=row['uid'], version=4),
                self._data[uuid.UUID(hex=row['data'], version=4)]
                )
        else:
            error_str = "Trying to get an non existing cell with id: {}"
            raise ValueError(error_str.format(c_uid))

    def add_point(self, point):
        """ Adds a new point to the mesh container.

        Parameters
        ----------
        point : Point
            Point to be added to the mesh container

        Raises
        ------
        KeyError
            If other point with the same uid was already
            in the mesh

        """

        if point.uid is None:
            point.uid = self._generate_uid()

        for row in self._group.points.where(
                'uid == value', condvars={'value': point.uid.hex}):
            error_str = "Trying to add an already\
                existing point with uid" + str(point.uid)
            raise KeyError(error_str)

        row = self._group.points.row

        row['uid'] = point.uid.hex
        row['data'] = self._data.append(point.data).hex
        row['coordinates'] = point.coordinates

        row.append()
        self._group.points.flush()

        return point.uid

    def add_edge(self, edge):
        """ Adds a new edge to the mesh container.

        Parameters
        ----------
        edge : Edge
            Edge to be added to the mesh container

        Raises
        ------
        KeyError
            If other edge with the same uid was already
            in the mesh

        """

        if edge.uid is None:
            edge.uid = self._generate_uid()

        for row in self._group.edges.where(
                'uid == value', condvars={'value': edge.uid.hex}):
            error_str = "Trying to add an already\
                existing edge with uid" + str(edge.uid)
            raise KeyError(error_str)

        n = len(edge.points)

        row = self._group.edges.row

        row['uid'] = edge.uid.hex
        row['data'] = self._data.append(edge.data).hex
        row['n_points'] = n
        row['points_uids'] = [puid.hex for puid in
                               edge.points] + [0] * (MAX_POINTS_IN_EDGE-n)

        row.append()
        self._group.edges.flush()

        return edge.uid

    def add_face(self, face):
        """ Adds a new face to the mesh container.

        Parameters
        ----------
        face : Face
            Face to be added to the mesh container

        Raises
        ------
        KeyError
            If other face with the same uid was already
            in the mesh

        """

        if face.uid is None:
            face.uid = self._generate_uid()

        for row in self._group.faces.where(
                'uid == value', condvars={'value': face.uid.hex}):
            error_str = "Trying to add an already\
                existing face with uid" + str(face.uid)
            raise KeyError(error_str)

        n = len(face.points)

        row = self._group.faces.row

        row['uid'] = face.uid.hex
        row['data'] = self._data.append(face.data).hex
        row['n_points'] = n
        row['points_uids'] = [puid.hex for puid in
                               face.points] + [0] * (MAX_POINTS_IN_FACE-n)

        row.append()
        self._group.faces.flush()

        return face.uid

    def add_cell(self, cell):
        """ Adds a new cell to the mesh container.

        Parameters
        ----------
        cell : Cell
            Cell to be added to the mesh container

        Raises
        ------
        KeyError
            If other cell with the same uid was already
            in the mesh

        """

        if cell.uid is None:
            cell.uid = self._generate_uid()

        for row in self._group.cells.where(
                'uid == value', condvars={'value': cell.uid.hex}):
            error_str = "Trying to add an already\
                existing cell with uid" + str(cell.uid)
            raise KeyError(error_str)

        n = len(cell.points)

        row = self._group.cells.row

        row['uid'] = cell.uid.hex
        row['data'] = self._data.append(cell.data).hex
        row['n_points'] = n
        row['points_uids'] = [puid.hex for puid in
                               cell.points] + [0] * (MAX_POINTS_IN_CELL-n)

        row.append()
        self._group.cells.flush()

        return cell.uid

    def update_point(self, point):
        """ Updates the information of a point.

        Gets the mesh point identified by the same
        uid as the provided point and updates its information.

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
                'uid == value', condvars={'value': point.uid.hex}):
            row['coordinates'] = list(point.coordinates)
            self._data[uuid.UUID(hex=row['data'], version=4)] = point.data
            row.update()
            row._flush_mod_rows()
            return
        else:
            error_str = "Trying to update a non\
                existing point with uid: " + str(point.uid)
            raise KeyError(error_str)

    def update_edge(self, edge):
        """ Updates the information of an edge.

        Gets the mesh edge identified by the same
        uid as the provided edge and updates its information.

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
                'uid == value', condvars={'value': edge.uid.hex}):
            n = len(edge.points)
            row['points_uids'] = [puid.hex for puid in
                                   edge.points] + [0] * (MAX_POINTS_IN_EDGE-n)
            self._data[uuid.UUID(hex=row['data'], version=4)] = edge.data
            row.update()
            row._flush_mod_rows()
            return
        else:
            error_str = "Trying to update a non\
                existing edge with uid: " + str(edge.uid)
            raise KeyError(error_str)

    def update_face(self, face):
        """ Updates the information of a face.

        Gets the mesh face identified by the same
        uid as the provided face and updates its information.

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
                'uid == value', condvars={'value': face.uid.hex}):
            n = len(face.points)
            row['points_uids'] = [puid.hex for puid in
                                   face.points] + [0] * (MAX_POINTS_IN_FACE-n)
            self._data[uuid.UUID(hex=row['data'], version=4)] = face.data
            row.update()
            row._flush_mod_rows()
            return
        else:
            error_str = "Trying to update a none\
                existing face with uid: " + str(face.uid)
            raise KeyError(error_str)

    def update_cell(self, cell):
        """ Updates the information of a cell.

        Gets the mesh cell identified by the same
        uid as the provided cell and updates its information.

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
                'uid == value', condvars={'value': cell.uid.hex}):
            n = len(cell.points)
            row['points_uids'] = [puid.hex for puid in
                                   cell.points] + [0] * (MAX_POINTS_IN_CELL-n)
            self._data[uuid.UUID(hex=row['data'], version=4)] = cell.data
            row.update()
            row._flush_mod_rows()
            return
        else:
            error_str = "Trying to update an non\
                existing cell with uid: " + str(cell.uid)
            raise KeyError(error_str)

    def iter_points(self, point_uids=None):
        """ Returns an iterator over the selected points.

        Returns an interator over the points with uid in
        point_uids. If non of the uids in point_uids exists,
        an empty iterator is returned. If there is no uids
        inside point_uids, a iterator over all points of
        the mesh is returned insted.

        Parameters
        ----------
        point_uids : list of uint64, optional
            uids of the desired points, default empty

        Returns
        -------
        iter
            Iterator over the selected points

        """

        if point_uids is None:
            for row in self._group.points:
                yield Point(
                    tuple(row['coordinates']),
                    uuid.UUID(hex=row['uid'], version=4)
                )
        else:
            for point_uid in point_uids:
                yield self.get_point(point_uid)

    def iter_edges(self, edge_uids=None):
        """ Returns an iterator over the selected edges.

        Returns an interator over the edged with uid in
        edge_uid. If non of the uids in edge_uids exists,
        an empty iterator is returned. If there is no uids
        inside edge_uids, a iterator over all edges of
        the mesh is returned insted.

        Parameters
        ----------
        edge_uids : list of uint64, optional
            uids of the desired edges, default empty

        Returns
        -------
        iter
            Iterator over the selected edges

        """

        if edge_uids is None:
            for row in self._group.edges:
                yield Edge(
                    list(row['points_uids']),
                    uuid.UUID(hex=row['uid'], version=4)
                )
        else:
            for edge_uid in edge_uids:
                yield self.get_edge(edge_uid)

    def iter_faces(self, face_uids=None):
        """ Returns an iterator over the selected faces.

        Returns an interator over the faces with uid in
        face_uids. If non of the ids in face_uids exists,
        an empty iterator is returned. If there is no uids
        inside face_uids, a iterator over all faces of
        the mesh is returned insted.

        Parameters
        ----------
        face_uids : list of uint64, optional
            uids of the desired faces, default empty

        Returns
        -------
        iter
            Iterator over the selected faces

        """

        if face_uids is None:
            for row in self._group.faces:
                yield Face(
                    list(row['points_uids']),
                    uuid.UUID(hex=row['uid'], version=4)
                )
        else:
            for face_uid in face_uids:
                yield self.get_face(face_uid)

    def iter_cells(self, cell_uids=None):
        """ Returns an iterator over the selected cells.

        Returns an interator over the cells with uid in
        cell_uids. If non of the ids in cell_uids exists,
        an empty iterator is returned. If there is no uids
        inside cell_uids, a iterator over all cells of
        the mesh is returned insted.

        Parameters
        ----------
        cell_uids : list of uint64, optional
            Uuds of the desired cell, default empty

        Returns
        -------
        iter
            Iterator over the selected cells

        """

        if cell_uids is None:
            for row in self._group.cells:
                yield Cell(
                    list(row['points_uids']),
                    uuid.UUID(hex=row['uid'], version=4)
                )
        else:
            for cell_uid in cell_uids:
                yield self.get_cell(cell_uid)

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

    def _generate_uid(self):
        """ Provides and uid for the object

        Provides an uid as defined in the standard RFC 4122
        """

        return uuid.uuid4()

    def _create_points_table(self):
        """ Generates the table to sotre points """

        self._file.create_table(
            self._group, "points", _PointDescriptor)

    def _create_edges_table(self):
        """ Generates the table to sotre edges """

        self._file.create_table(
            self._group, "edges", _EdgeDescriptor)

    def _create_faces_table(self):
        """ Generates the table to sotre faces """

        self._file.create_table(
            self._group, "faces", _FaceDescriptor)

    def _create_cells_table(self):
        """ Generates the table to sotre cells """

        self._file.create_table(
            self._group, "cells", _CellDescriptor)

    def _create_data_table(self):
        """ Generates the table to sotre data

        This table stores the uuid asociated to a given
        data record.

        """

        self._data = DataContainerTable(self._group, 'data')
