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

from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA

from simphony.io.data_container_table import DataContainerTable
from simphony.io.indexed_data_container_table import IndexedDataContainerTable

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


class H5Mesh(object):
    """ H5Mesh.

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
        Data relative to the mesh
    name : String
        Name of the mesh

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
        self._data = IndexedDataContainerTable(group, 'data')
        self._uidData = DataContainerTable(self._group, 'item_data')

        if "points" not in self._group:
            self._create_points_table()

        if "edges" not in self._group:
            self._create_edges_table()

        if "faces" not in self._group:
            self._create_faces_table()

        if "cells" not in self._group:
            self._create_cells_table()

        self._items_count = {
            CUBA.POINT: lambda: self._group.points,
            CUBA.EDGE: lambda: self._group.edges,
            CUBA.FACE: lambda: self._group.faces,
            CUBA.CELL: lambda: self._group.cells
        }

    @property
    def name(self):
        return self._group._v_name

    @name.setter
    def name(self, value):
        self._group._f_rename(value)

    @property
    def data(self):
        if len(self._data) == 1:
            return self._data[0]
        else:
            return DataContainer()

    @data.setter
    def data(self, value):
        if len(self._data) == 0:
            self._data.append(value)
        else:
            self._data[0] = value

    def get_point(self, uid):
        """ Returns a point with a given uid.

        Returns the point stored in the mesh
        identified by uid. If such point do not
        exists an exception is raised.

        Parameters
        ----------
        uid : UUID
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
        if not hasattr(uid, 'hex'):
            message = 'Expected type for `uid` is uuid.UUID but received {!r}'
            raise TypeError(message.format(type(uid)))

        for row in self._group.points.where(
                'uid == value', condvars={'value': uid.hex}):
            return Point(
                coordinates=tuple(row['coordinates']),
                uid=uuid.UUID(hex=row['uid'], version=4),
                data=self._uidData[uuid.UUID(hex=row['data'], version=4)])
        else:
            error_str = "Trying to get an non existing point with uid: {}"
            raise KeyError(error_str.format(uid))

    def get_edge(self, uid):
        """ Returns an edge with a given uid.

        Returns the edge stored in the mesh
        identified by uid. If such edge do not
        exists a exception is raised.

        Parameters
        ----------
        uid : UUID
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
        if not hasattr(uid, 'hex'):
            message = 'Expected type for `uid` is uuid.UUID but received {!r}'
            raise TypeError(message.format(type(uid)))

        for row in self._group.edges.where(
                'uid == value', condvars={'value': uid.hex}):
            return Edge(
                points=tuple(
                    uuid.UUID(hex=pb, version=4)
                    for pb in row['points_uids'][0:row['n_points']]),
                uid=uuid.UUID(hex=row['uid'], version=4),
                data=self._uidData[uuid.UUID(hex=row['data'], version=4)])
        else:
            error_str = "Trying to get an non existing edge with uid: {}"
            raise KeyError(error_str.format(uid))

    def get_face(self, uid):
        """ Returns an face with a given uid.

        Returns the face stored in the mesh
        identified by uid. If such face do not
        exists a exception is raised.

        Parameters
        ----------
        uid : UUID
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
        if not hasattr(uid, 'hex'):
            message = 'Expected type for `uid` is uuid.UUID but received {!r}'
            raise TypeError(message.format(type(uid)))

        for row in self._group.faces.where(
                'uid == value', condvars={'value': uid.hex}):
            return Face(
                uid=uuid.UUID(hex=row['uid'], version=4),
                points=tuple(
                    uuid.UUID(hex=pb, version=4)
                    for pb in row['points_uids'][:row['n_points']]),
                data=self._uidData[uuid.UUID(hex=row['data'], version=4)])
        else:
            error_str = "Trying to get an non existing face with uid: {}"
            raise KeyError(error_str.format(uid))

    def get_cell(self, uid):
        """ Returns an cell with a given uid.

        Returns the cell stored in the mesh
        identified by uid . If such cell do not
        exists a exception is raised.

        Parameters
        ----------
        uid : UUID
            uid of the desired cell.

        Returns
        -------
        Cell
            Cell identified by uid

        Raises
        ------
        Exception
            If the cell identified by uid was not found

        """
        if not hasattr(uid, 'hex'):
            message = 'Expected type for `uid` is uuid.UUID but received {!r}'
            raise TypeError(message.format(type(uid)))

        for row in self._group.cells.where(
                'uid == value', condvars={'value': uid.hex}):
            return Cell(
                points=tuple(
                    uuid.UUID(hex=pb, version=4)
                    for pb in row['points_uids'][0:row['n_points']]),
                uid=uuid.UUID(hex=row['uid'], version=4),
                data=self._uidData[uuid.UUID(hex=row['data'], version=4)])
        else:
            error_str = "Trying to get an non existing cell with id: {}"
            raise KeyError(error_str.format(uid))

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
            error_str = "Trying to add an already existing point with uid {}"
            raise ValueError(error_str.format(point.uid))

        row = self._group.points.row

        row['uid'] = point.uid.hex
        row['data'] = self._uidData.append(point.data).hex
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
        else:
            for row in self._group.edges.where(
                    'uid == value', condvars={'value': edge.uid.hex}):
                message = "Trying to add an already existing edge with uid {}"
                raise ValueError(message.format(edge.uid))

        n = len(edge.points)

        row = self._group.edges.row

        row['uid'] = edge.uid.hex
        row['data'] = self._uidData.append(edge.data).hex
        row['n_points'] = n
        row['points_uids'] = [puid.hex for puid in
                              edge.points] + [''] * (MAX_POINTS_IN_EDGE-n)

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
        else:
            for row in self._group.faces.where(
                    'uid == value', condvars={'value': face.uid.hex}):
                message = "Trying to add an already existing face with uid {}"
                raise ValueError(message.format(face.uid))

        n = len(face.points)

        row = self._group.faces.row

        row['uid'] = face.uid.hex
        row['data'] = self._uidData.append(face.data).hex
        row['n_points'] = n
        row['points_uids'] = [puid.hex for puid in
                              face.points] + [''] * (MAX_POINTS_IN_FACE-n)

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
        else:
            for row in self._group.cells.where(
                    'uid == value', condvars={'value': cell.uid.hex}):
                message = "Trying to add an already existing cell with uid"
                raise ValueError(message.format(cell.uid))

        n = len(cell.points)

        row = self._group.cells.row

        row['uid'] = cell.uid.hex
        row['data'] = self._uidData.append(cell.data).hex
        row['n_points'] = n
        row['points_uids'] = [puid.hex for puid in
                              cell.points] + [''] * (MAX_POINTS_IN_CELL-n)

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
            self._uidData[uuid.UUID(hex=row['data'], version=4)] = point.data
            row.update()
            row._flush_mod_rows()
            return
        else:
            error_str = "Trying to update a non existing point with uid: {}"
            raise ValueError(error_str.format(point.uid))

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
            row['n_points'] = n
            row['points_uids'] = [puid.hex for puid in
                                  edge.points] + [0] * (MAX_POINTS_IN_EDGE-n)
            self._uidData[uuid.UUID(hex=row['data'], version=4)] = edge.data
            row.update()
            row._flush_mod_rows()
            return
        else:
            error_str = "Trying to update a non existing edge with uid: "
            raise ValueError(error_str.format(edge.uid))

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
            row['n_points'] = n
            row['points_uids'] = [puid.hex for puid in
                                  face.points] + [0] * (MAX_POINTS_IN_FACE-n)
            self._uidData[uuid.UUID(hex=row['data'], version=4)] = face.data
            row.update()
            row._flush_mod_rows()
            return
        else:
            error_str = "Trying to update a none existing face with uid: {}"
            raise ValueError(error_str.format(face.uid))

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
            row['n_points'] = n
            row['points_uids'] = [puid.hex for puid in
                                  cell.points] + [0] * (MAX_POINTS_IN_CELL-n)
            self._uidData[uuid.UUID(hex=row['data'], version=4)] = cell.data
            row.update()
            row._flush_mod_rows()
            return
        else:
            error_str = "Trying to update an non existing cell with uid: {}"
            raise ValueError(error_str.format(cell.uid))

    def iter_points(self, uids=None):
        """ Returns an iterator over points.

        Parameters
        ----------
        uids : iterable of uuid.UUID or None
            When the uids are provided, then the points are returned in
            the same order the uids are returned by the iterable. If uids is
            None, then all points are returned by the interable and there
            is no restriction on the order that they are returned.

        Returns
        -------
        iter
            Iterator over the points

        """
        if uids is None:
            for row in self._group.points:
                yield Point(
                    tuple(row['coordinates']),
                    uuid.UUID(hex=row['uid'], version=4),
                    self._uidData[uuid.UUID(hex=row['data'], version=4)]
                )
        else:
            for uid in uids:
                yield self.get_point(uid)

    def iter_edges(self, uids=None):
        """ Returns an iterator over edges.

        Parameters
        ----------
        uids : iterable of uuid.UUID  or None
            When the uids are provided, then the edges are returned in the
            same order the uids are returned by the iterable. If uids is None,
            then all edges are returned by the interable and there is no
            restriction on the order that they are returned.

        Returns
        -------
        iter
            Iterator over the selected edges

        """
        if uids is None:
            for row in self._group.edges:
                yield Edge(
                    list(uuid.UUID(hex=pb, version=4) for pb in
                         row['points_uids'][0:row['n_points']]),
                    uuid.UUID(hex=row['uid'], version=4),
                    self._uidData[uuid.UUID(hex=row['data'], version=4)]
                )
        else:
            for uid in uids:
                yield self.get_edge(uid)

    def iter_faces(self, uids=None):
        """ Returns an iterator over faces.

        Parameters
        ----------
        uids : iterable of uuid.UUID  or None
            When the uids are provided, then the faces are returned in the
            same order the uids are returned by the iterable. If uids is None,
            then all faces are returned by the interable and there is no
            restriction on the order that they are returned.

        Returns
        -------
        iter
            Iterator over the faces

        """
        if uids is None:
            for row in self._group.faces:
                yield Face(
                    list(uuid.UUID(hex=pb, version=4) for pb in
                         row['points_uids'][0:row['n_points']]),
                    uuid.UUID(hex=row['uid'], version=4),
                    self._uidData[uuid.UUID(hex=row['data'], version=4)]
                )
        else:
            for uid in uids:
                yield self.get_face(uid)

    def iter_cells(self, uids=None):
        """ Returns an iterator over cells.

        Parameters
        ----------
        uids : iterable of uuid.UUID  or None
            When the uids are provided, then the cells are returned in the same
            order the uids are returned by the iterable. If uids is None, then
            all cells are returned by the interable and there is no restriction
            on the order that they are returned.

        Returns
        -------
        iter
            Iterator over the selected cells

        """
        if uids is None:
            for row in self._group.cells:
                yield Cell(
                    list(uuid.UUID(hex=pb, version=4) for pb in
                         row['points_uids'][0:row['n_points']]),
                    uuid.UUID(hex=row['uid'], version=4),
                    self._uidData[uuid.UUID(hex=row['data'], version=4)]
                )
        else:
            for uid in uids:
                yield self.get_cell(uid)

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

    def count_of(self, item_type):
        """ Return the count of item_type in the container.

        Parameter
        ---------
        item_type : CUBA
            The CUBA enum of the type of the items to return the count of.

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
