import os
import tempfile
import shutil
import unittest

from functools import partial

from simphony.testing.utils import compare_data_containers

from simphony.cuds.mesh import Mesh
from simphony.cuds.mesh import Point
from simphony.cuds.mesh import Edge
from simphony.cuds.mesh import Face
from simphony.cuds.mesh import Cell

from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer

from simphony.io.h5_cuds import H5CUDS


class TestH5Mesh(unittest.TestCase):

    def setUp(self):

        self.addTypeEqualityFunc(
            DataContainer, partial(compare_data_containers, testcase=self))

        self.temp_dir = tempfile.mkdtemp()

        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.file = H5CUDS.open(self.filename)
        self.mesh = self.file.add_mesh(Mesh(name="test"))

        self.pids = []
        self.points = [
            Point(
                (0.0, 0.0, 0.0),
                data=DataContainer({CUBA.VELOCITY: (0, 0, 0)})),
            Point(
                (1.0, 0.0, 0.0),
                data=DataContainer({CUBA.VELOCITY: (0, 0, 0)})),
            Point(
                (0.0, 1.0, 0.0),
                data=DataContainer({CUBA.VELOCITY: (0, 0, 0)})),
            Point(
                (0.0, 0.0, 1.0),
                data=DataContainer({CUBA.VELOCITY: (0, 0, 0)})),
            Point(
                (1.0, 0.0, 1.0),
                data=DataContainer({CUBA.VELOCITY: (0, 0, 0)})),
            Point(
                (0.0, 1.0, 1.0),
                data=DataContainer({CUBA.VELOCITY: (0, 0, 0)}))
        ]

    def tearDown(self):
        if os.path.exists(self.filename):
            self.file.close()
        shutil.rmtree(self.temp_dir)

    def test_emtpy_edges(self):
        """ Checks that the list of edges is empty

        """

        self.assertFalse(self.mesh.has_edges())

    def test_emtpy_faces(self):
        """ Checks that the list of faces is empty

        """

        self.assertFalse(self.mesh.has_faces())

    def test_emtpy_cells(self):
        """ Checks that the list of cells is empty

        """

        self.assertFalse(self.mesh.has_cells())

    def test_add_point(self):
        """ Check that a point can be added correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:1]]

        self.assertIsNotNone(self.mesh.get_point(puids[0]))

    def test_add_edge(self):
        """ Check that an edge can be added correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:2]]

        edge = Edge(puids[0:2])

        euids = [self.mesh.add_edge(edge)]

        self.assertIsNotNone(self.mesh.get_edge(euids[0]))

    def test_add_face(self):
        """ Check that a face can be added correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:3]]

        face = Face(puids[0:3])

        fuids = [self.mesh.add_face(face)]

        self.assertIsNotNone(self.mesh.get_face(fuids[0]))

    def test_add_cell(self):
        """ Check that a cell can be added correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:4]]

        cell = Cell(puids[0:4])

        cuids = [self.mesh.add_cell(cell)]

        self.assertIsNotNone(self.mesh.get_cell(cuids[0]))

    def test_add_duplicated_point(self):
        """ Check that a point can be added correctly

        """

        self.mesh.add_point(self.points[0])
        self.assertRaises(KeyError, self.mesh.add_point, self.points[0])

    def test_add_duplicated_edge(self):
        """ Check that an edge can be added correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:2]]

        edges = [
            Edge(puids[0:2])
        ]

        self.mesh.add_edge(edges[0])
        self.assertRaises(KeyError, self.mesh.add_edge, edges[0])

    def test_add_duplicated_face(self):
        """ Check that a face can be added correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:3]]

        faces = [
            Face(puids[0:3])
        ]

        self.mesh.add_face(faces[0])
        self.assertRaises(KeyError, self.mesh.add_face, faces[0])

    def test_add_duplicated_cell(self):
        """ Check that a cell can be added correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:4]]

        cells = [
            Cell(puids[0:4])
        ]

        self.mesh.add_cell(cells[0])
        self.assertRaises(KeyError, self.mesh.add_cell, cells[0])

    def test_non_emtpy_edges(self):
        """ Checks that the list of edges is not empty

        """

        puids = [self.mesh.add_point(point) for point in self.points[:2]]

        edge = Edge(puids[0:2])

        self.mesh.add_edge(edge)

        self.assertTrue(self.mesh.has_edges())

    def test_non_emtpy_faces(self):
        """ Checks that the list of faces is not empty

        """

        puids = [self.mesh.add_point(point) for point in self.points[:3]]

        face = Face(puids[0:3])

        self.mesh.add_face(face)

        self.assertTrue(self.mesh.has_faces())

    def test_non_emtpy_cells(self):
        """ Checks that the list of cells is not empty

        """

        puids = [self.mesh.add_point(point) for point in self.points[:4]]

        cell = Cell(puids[0:4])

        self.mesh.add_cell(cell)

        self.assertTrue(self.mesh.has_cells())

    def test_get_point(self):
        """ Check that a point can be retrieved correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:1]]

        point_ret = self.mesh.get_point(puids[0])

        self.assertTrue(isinstance(point_ret, Point))
        self.assertEqual(puids[0], point_ret.uid)
        self.assertItemsEqual(
            self.points[0].coordinates,
            point_ret.coordinates
        )
        for key, value in self.points[0].data.iteritems():
            self.assertItemsEqual(point_ret.data[key], value)

    def test_get_edge(self):
        """ Check that an edge can be retrieved correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:2]]

        edges = [
            Edge(puids[:]),
        ]

        euids = [self.mesh.add_edge(edge) for edge in edges]

        edge_ret = self.mesh.get_edge(euids[0])

        self.assertTrue(isinstance(edge_ret, Edge))
        self.assertEqual(euids[0], edge_ret.uid)
        self.assertItemsEqual(
            edges[0].points,
            edge_ret.points
        )
        for key, value in edges[0].data.iteritems():
            self.assertItemsEqual(edge_ret.data[key], value)

    def test_get_face(self):
        """ Check that a face can be retrieved correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:3]]

        faces = [
            Face(puids[:])
        ]

        fuids = [self.mesh.add_face(face) for face in faces]

        face_ret = self.mesh.get_face(fuids[0])

        self.assertTrue(isinstance(face_ret, Face))
        self.assertEqual(fuids[0], face_ret.uid)
        self.assertItemsEqual(
            faces[0].points,
            face_ret.points
        )
        for key, value in faces[0].data.iteritems():
            self.assertItemsEqual(face_ret.data[key], value)

    def test_get_cell(self):
        """ Check that a cell can be retrieved correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:4]]

        cells = [
            Cell(puids[:])
            ]

        cuids = [self.mesh.add_cell(cell) for cell in cells]

        cell_ret = self.mesh.get_cell(cuids[0])

        self.assertTrue(isinstance(cell_ret, Cell))
        self.assertEqual(cuids[0], cell_ret.uid)
        self.assertItemsEqual(
            cells[0].points,
            cell_ret.points
        )
        for key, value in cells[0].data.iteritems():
            self.assertItemsEqual(cell_ret.data[key], value)

    def test_get_all_points_iterator(self):
        """ Checks the point iterator

        Checks that an interator over all
        the edges of the mesh is returned
        when the function iter_edges is called
        without arguments

        """

        puids = [self.mesh.add_point(point) for point in self.points[:3]]

        ipoints = self.mesh.iter_points()

        ipoints_id = [point.uid for point in ipoints]

        self.assertItemsEqual(ipoints_id, puids)

    def test_get_all_edges_iterator(self):
        """ Checks the edge iterator

        Checks that an interator over all
        the edges of the mesh is returned
        when the function iter_edges is called
        without arguments

        """

        puids = [self.mesh.add_point(point) for point in self.points[:3]]

        edges = [
            Edge(puids[0:2]),
            Edge(puids[1:3])
        ]

        euids = [self.mesh.add_edge(edge) for edge in edges]

        iedges = self.mesh.iter_edges()

        iedges_id = [edge.uid for edge in iedges]

        self.assertItemsEqual(iedges_id, euids)

        mesh_points = [p.uid for p in self.mesh.iter_points()]
        edge_points = []

        for edge in self.mesh.iter_edges():
            for p in edge.points:
                edge_points.append(p)

        self.assertItemsEqual(set(mesh_points), set(edge_points))

    def test_get_all_faces_iterator(self):
        """ Checks the face iterator

        Checks that an interator over all
        the faces of the mesh is returned
        when the function iter_faces is called
        without arguments

        """

        puids = [self.mesh.add_point(point) for point in self.points[:4]]

        faces = [
            Face(puids[0:3]),
            Face(puids[1:4])
        ]

        fuids = [self.mesh.add_face(face) for face in faces]

        ifaces = self.mesh.iter_faces()

        ifaces_id = [face.uid for face in ifaces]

        self.assertItemsEqual(fuids, ifaces_id)

        mesh_points = [p.uid for p in self.mesh.iter_points()]
        face_points = []

        for face in self.mesh.iter_faces():
            for p in face.points:
                face_points.append(p)

        self.assertItemsEqual(set(mesh_points), set(face_points))

    def test_get_all_cells_iterator(self):
        """ Checks the cell iterators

        Checks that an interator over all
        the cells of the mesh is returned
        when the function iter_cells is called
        without arguments

        """

        puids = [self.mesh.add_point(point) for point in self.points[:5]]

        cells = [
            Cell(puids[0:4]),
            Cell(puids[1:5])
            ]

        cuids = [self.mesh.add_cell(cell) for cell in cells]

        icells = self.mesh.iter_cells()

        icells_id = [cell.uid for cell in icells]

        self.assertItemsEqual(icells_id, cuids)

        mesh_points = [p.uid for p in self.mesh.iter_points()]
        cell_points = []

        for cell in self.mesh.iter_cells():
            for p in cell.points:
                cell_points.append(p)

        self.assertItemsEqual(set(mesh_points), set(cell_points))

    def test_get_all_points_iterator_with_data(self):
        """ Checks the point iterator

        Checks that an interator over all
        the points of the mesh is returned
        when the function iter_points is called
        without arguments and its data is correctly retrieved

        """

        puids = [self.mesh.add_point(point) for point in self.points[:3]]

        ipoints = self.mesh.iter_points()

        ipoints_id = [point.uid for point in ipoints]
        first_point = self.mesh.iter_points().next()

        self.assertItemsEqual(ipoints_id, puids)
        self.assertIsNot(len(first_point.data), 0)

        self.assertEqual(first_point.data, DataContainer(VELOCITY=(0, 0, 0)))

    def test_get_all_edges_iterator_with_data(self):
        """ Checks the edge iterator

        Checks that an interator over all
        the edges of the mesh is returned
        when the function iter_edges is called
        without arguments and its data is correctly retrieved

        """

        puids = [self.mesh.add_point(point) for point in self.points[:3]]

        edges = [
            Edge(puids[0:2], data=DataContainer({CUBA.VELOCITY: (0, 0, 0)}))
        ]

        euids = [self.mesh.add_edge(edge) for edge in edges]

        iedges = self.mesh.iter_edges()

        iedges_id = [edge.uid for edge in iedges]
        first_edge = self.mesh.iter_edges().next()

        self.assertItemsEqual(iedges_id, euids)
        self.assertIsNot(len(first_edge.data), 0)

        self.assertEqual(first_edge.data, DataContainer(VELOCITY=(0, 0, 0)))

    def test_get_all_faces_iterator_with_data(self):
        """ Checks the face iterator

        Checks that an interator over all
        the faces of the mesh is returned
        when the function iter_faces is called
        without arguments and its data is correctly retrieved

        """

        puids = [self.mesh.add_point(point) for point in self.points[:4]]

        faces = [
            Face(puids[0:3], data=DataContainer({CUBA.VELOCITY: (0, 0, 0)}))
        ]

        fuids = [self.mesh.add_face(face) for face in faces]

        ifaces = self.mesh.iter_faces()

        ifaces_id = [face.uid for face in ifaces]
        first_face = self.mesh.iter_faces().next()

        self.assertItemsEqual(fuids, ifaces_id)
        self.assertIsNot(len(first_face.data), 0)

        self.assertEqual(first_face.data, DataContainer(VELOCITY=(0, 0, 0)))

    def test_get_all_cells_iterator_with_data(self):
        """ Checks the cell iterators

        Checks that an interator over all
        the cells of the mesh is returned
        when the function iter_cells is called
        without arguments and its data is correctly retrieved

        """

        puids = [self.mesh.add_point(point) for point in self.points[:5]]

        cells = [
            Cell(puids[0:4], data=DataContainer({CUBA.VELOCITY: (0, 0, 0)}))
            ]

        cuids = [self.mesh.add_cell(cell) for cell in cells]

        icells = self.mesh.iter_cells()

        icells_id = [cell.uid for cell in icells]
        first_cell = self.mesh.iter_cells().next()

        self.assertItemsEqual(icells_id, cuids)
        self.assertIsNot(len(first_cell.data), 0)

        self.assertEqual(first_cell.data, DataContainer(VELOCITY=(0, 0, 0)))

    def test_get_subset_edges_iterator(self):
        """ Checks the edge iterator

        Checks that an interator over a subset of
        the edges of the mesh is returned
        when the function iter_edges is called
        selecting a list of uid's

        """

        puids = [self.mesh.add_point(point) for point in self.points[:4]]

        edges = [
            Edge(puids[0:2]),
            Edge(puids[2:3]),
            Edge(puids[3:4])
            ]

        euids = [self.mesh.add_edge(edge) for edge in edges]

        iedges = self.mesh.iter_edges([euids[0], euids[2]])

        source_id = [euids[0], euids[2]]
        iedges_id = [edge.uid for edge in iedges]

        self.assertItemsEqual(source_id, iedges_id)

        mesh_points = [p.uid for p in self.mesh.iter_points()]
        edge_points = []

        for edge in self.mesh.iter_edges():
            for p in edge.points:
                edge_points.append(p)

        self.assertItemsEqual(set(mesh_points), set(edge_points))

    def test_get_subset_faces_iterator(self):
        """ Checks the face iterator

        Checks that an interator over a subset of
        the faces of the mesh is returned
        when the function iter_faces is called
        selecting a list of uid's

        """

        puids = [self.mesh.add_point(point) for point in self.points[:5]]

        faces = [
            Face(puids[0:3]),
            Face(puids[1:4]),
            Face(puids[2:5])
            ]

        fuids = [self.mesh.add_face(face) for face in faces]

        ifaces = self.mesh.iter_faces([fuids[0], fuids[2]])

        source_id = [fuids[0], fuids[2]]
        ifaces_id = [face.uid for face in ifaces]

        self.assertItemsEqual(source_id, ifaces_id)

        mesh_points = [p.uid for p in self.mesh.iter_points()]
        face_points = []

        for face in self.mesh.iter_faces():
            for p in face.points:
                face_points.append(p)

        self.assertItemsEqual(set(mesh_points), set(face_points))

    def test_get_subset_cells_iterator(self):
        """ Checks the cell iterator

        Checks that an interator over a subset of
        the cells of the mesh is returned
        when the function iter_cells is called
        selecting a list of uid's

        """

        puids = [self.mesh.add_point(point) for point in self.points[:6]]

        cells = [
            Cell(puids[0:4]),
            Cell(puids[1:5]),
            Cell(puids[2:6])
            ]

        cuids = [self.mesh.add_cell(cell) for cell in cells]

        icells = self.mesh.iter_cells([cuids[0], cuids[2]])

        source_id = [cuids[0], cuids[2]]
        icells_id = [cell.uid for cell in icells]

        self.assertItemsEqual(source_id, icells_id)

        mesh_points = [p.uid for p in self.mesh.iter_points()]
        cell_points = []

        for cell in self.mesh.iter_cells():
            for p in cell.points:
                cell_points.append(p)

        self.assertItemsEqual(set(mesh_points), set(cell_points))

    def test_update_point(self):
        """ Check that a point can be updated correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:1]]

        point_ret = self.mesh.get_point(puids[0])
        point_ret.coordinates = [-1.0, -1.0, -1.0]
        self.mesh.update_point(point_ret)

        point_upd = self.mesh.get_point(puids[0])

        self.assertItemsEqual(point_upd.coordinates, point_ret.coordinates)

    def test_update_edge(self):
        """ Check that an edge can be updated correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:3]]

        edges = [
            Edge(puids[0:2])
        ]

        euids = [self.mesh.add_edge(edge) for edge in edges]

        edge_ret = self.mesh.get_edge(euids[0])
        edge_ret.points[1] = puids[2]
        self.mesh.update_edge(edge_ret)

        edge_upd = self.mesh.get_edge(euids[0])

        self.assertItemsEqual(edge_upd.points, edge_ret.points)

    def test_update_face(self):
        """ Check that a face can be updated correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:4]]

        faces = [
            Face(puids[0:3])
        ]

        fuids = [self.mesh.add_face(face) for face in faces]

        face_ret = self.mesh.get_face(fuids[0])
        face_ret.points[2] = puids[3]
        self.mesh.update_face(face_ret)

        face_upd = self.mesh.get_face(fuids[0])

        self.assertItemsEqual(face_upd.points, face_ret.points)

    def test_update_cell(self):
        """ Check that a cell can be updated correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:5]]

        cells = [
            Cell(puids[0:4])
        ]

        cuids = [self.mesh.add_cell(cell) for cell in cells]

        cell_ret = self.mesh.get_cell(cuids[0])
        cell_ret.points[3] = puids[4]
        self.mesh.update_cell(cell_ret)

        cell_upd = self.mesh.get_cell(cuids[0])

        self.assertItemsEqual(cell_upd.points, cell_ret.points)

    def test_update_point_data(self):
        """ Check that the data of a point can be updated correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:1]]

        point_ret = self.mesh.get_point(puids[0])
        point_ret.data[CUBA.VELOCITY] = (42, 42, 42)

        self.mesh.update_point(point_ret)

        point_upd = self.mesh.get_point(puids[0])

        self.assertItemsEqual(
            point_upd.data[CUBA.VELOCITY],
            point_ret.data[CUBA.VELOCITY])

    def test_update_edge_data(self):
        """ Check that the data of an edge can be updated correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:3]]

        edges = [
            Edge(puids[0:2])
        ]

        euids = [self.mesh.add_edge(edge) for edge in edges]

        edge_ret = self.mesh.get_edge(euids[0])
        edge_ret.data[CUBA.VELOCITY] = (42, 42, 42)

        self.mesh.update_edge(edge_ret)

        edge_upd = self.mesh.get_edge(euids[0])

        self.assertItemsEqual(
            edge_upd.data[CUBA.VELOCITY],
            edge_ret.data[CUBA.VELOCITY])

    def test_update_face_data(self):
        """ Check that the data of a face can be updated correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:4]]

        faces = [
            Face(puids[0:3])
        ]

        fuids = [self.mesh.add_face(face) for face in faces]

        face_ret = self.mesh.get_face(fuids[0])
        face_ret.data[CUBA.VELOCITY] = (42, 42, 42)

        self.mesh.update_face(face_ret)

        face_upd = self.mesh.get_face(fuids[0])

        self.assertItemsEqual(
            face_upd.data[CUBA.VELOCITY],
            face_ret.data[CUBA.VELOCITY])

    def test_update_cell_data(self):
        """ Check that the data of a cell can be updated correctly

        """

        puids = [self.mesh.add_point(point) for point in self.points[:5]]

        cells = [
            Cell(puids[0:4])
        ]

        cuids = [self.mesh.add_cell(cell) for cell in cells]

        cell_ret = self.mesh.get_cell(cuids[0])
        cell_ret.data[CUBA.VELOCITY] = (42, 42, 42)

        self.mesh.update_cell(cell_ret)

        cell_upd = self.mesh.get_cell(cuids[0])

        self.assertItemsEqual(
            cell_upd.data[CUBA.VELOCITY],
            cell_ret.data[CUBA.VELOCITY])

if __name__ == '__main__':
    unittest.main()
