""" test_mesh module

This module contains the unitary tests for the
mesh module functionalities

"""

import unittest
from simphony.cuds.mesh import Mesh
from simphony.cuds.mesh import Point
from simphony.cuds.mesh import Edge
from simphony.cuds.mesh import Face
from simphony.cuds.mesh import Cell


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        """ Creates an empty mesh to perform the tests

        Creates an empty mesh and and a set of points
        to tests all the mesh methods

        """
        self.mesh = Mesh()
        self.points = [Point(0, (0.0, 0.0, 0.0), 0),
                       Point(1, (1.0, 0.0, 0.0), 0),
                       Point(2, (0.0, 1.0, 0.0), 0),
                       Point(3, (0.0, 0.0, 1.0), 0),
                       Point(4, (1.0, 0.0, 1.0), 0)
                       ]

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

        point = self.points[0]

        self.mesh.add_point(point)

        self.assertTrue(len(self.mesh.points.keys()))

    def test_add_edge(self):
        """ Check that an edge can be added correctly

        """

        points = [
            self.points[0],
            self.points[1]
            ]

        edge = Edge(0, points, 0)

        self.mesh.add_edge(edge)

        self.assertTrue(len(self.mesh.edges.keys()))

    def test_add_face(self):
        """ Check that a face can be added correctly

        """

        points = [
            self.points[0],
            self.points[1],
            self.points[2]
            ]

        face = Face(0, points, 0)

        self.mesh.add_face(face)

        self.assertTrue(len(self.mesh.faces.keys()))

    def test_add_cell(self):
        """ Check that a cell can be added correctly

        """

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        cell = Cell(0, points, 0)

        self.mesh.add_cell(cell)

        self.assertTrue(len(self.mesh.cells.keys()))

    def test_add_wrong_type_point(self):
        """ Check that a only points can be added to the point list

        """

        points = [
            self.points[0],
            self.points[1]
            ]

        edge = Edge(0, points, 0)

        with self.assertRaises(Exception) as cm:
            self.mesh.add_point(edge)

        self.assertIsInstance(cm.exception, TypeError)

    def test_add_wrong_type_edge(self):
        """ Check that a only edges can be added to the edge list

        """

        point = self.points[0]

        with self.assertRaises(Exception) as cm:
            self.mesh.add_edge(point)

        self.assertIsInstance(cm.exception, TypeError)

    def test_add_wrong_type_face(self):
        """ Check that a only faces can be added to the face list

        """

        point = self.points[0]

        with self.assertRaises(Exception) as cm:
            self.mesh.add_face(point)

        self.assertIsInstance(cm.exception, TypeError)

    def test_add_wrong_type_cell(self):
        """ Check that a only cells can be added to the cell list

        """

        point = self.points[0]

        with self.assertRaises(Exception) as cm:
            self.mesh.add_cell(point)

        self.assertIsInstance(cm.exception, TypeError)

    def test_non_emtpy_edges(self):
        """ Checks that the list of edges is not empty

        """

        points = [
            self.points[0],
            self.points[1]
            ]

        edge = Edge(0, points, 0)

        self.mesh.add_edge(edge)

        self.assertTrue(self.mesh.has_edges())

    def test_non_emtpy_faces(self):
        """ Checks that the list of faces is not empty

        """

        points = [
            self.points[0],
            self.points[1],
            self.points[2]
            ]

        face = Face(0, points, 0)

        self.mesh.add_face(face)

        self.assertTrue(self.mesh.has_faces())

    def test_non_emtpy_cells(self):
        """ Checks that the list of cells is not empty

        """

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        cell = Cell(0, points, 0)

        self.mesh.add_cell(cell)

        self.assertTrue(self.mesh.has_cells())

    def test_get_point(self):
        """ Check that a point can be retrieved correctly

        """

        point = self.points[0]

        self.mesh.add_point(point)

        point_ret = self.mesh.get_point(0)

        self.assertTrue(isinstance(point_ret, Point))
        self.assertEqual(point.id, point_ret.id)

    def test_get_edge(self):
        """ Check that an edge can be retrieved correctly

        """

        points = [
            self.points[0],
            self.points[1]
            ]

        edge = Edge(0, points, 0)

        self.mesh.add_edge(edge)

        edge_ret = self.mesh.get_edge(0)

        self.assertTrue(isinstance(edge_ret, Edge))
        self.assertEqual(edge.id, edge_ret.id)

    def test_get_face(self):
        """ Check that a point can be retrieved correctly

        """

        points = [
            self.points[0],
            self.points[1],
            self.points[2]
            ]

        face = Face(0, points, 0)

        self.mesh.add_face(face)

        face_ret = self.mesh.get_face(0)

        self.assertTrue(isinstance(face_ret, Face))
        self.assertEqual(face.id, face_ret.id)

    def test_get_cell(self):
        """ Check that a point can be retrieved correctly

        """

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        cell = Cell(0, points, 0)

        self.mesh.add_cell(cell)

        cell_ret = self.mesh.get_cell(0)

        self.assertTrue(isinstance(cell_ret, Cell))
        self.assertEqual(cell.id, cell_ret.id)

    def test_get_all_edges_iterator(self):
        """ Checks the edge iterator

        Checks that an interator over all
        the edges of the mesh is returned
        when the function iter_edges is called
        without arguments

        """

        pointsA = [
            self.points[0],
            self.points[1]
            ]
        pointsB = [
            self.points[1],
            self.points[2]
            ]

        edgeA = Edge(0, pointsA, 0)
        edgeB = Edge(1, pointsB, 0)

        self.mesh.add_edge(edgeA)
        self.mesh.add_edge(edgeB)

        edges = self.mesh.iter_edges()

        source_id = [0, 1]
        edges_id = [edge.id for edge in edges]

        self.assertItemsEqual(source_id, edges_id)

    def test_get_all_faces_iterator(self):
        """ Checks the face iterator

        Checks that an interator over all
        the faces of the mesh is returned
        when the function iter_faces is called
        without arguments

        """

        pointsA = [
            self.points[0],
            self.points[1],
            self.points[2]
            ]
        pointsB = [
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        faceA = Face(0, pointsA, 0)
        faceB = Face(1, pointsB, 0)

        self.mesh.add_face(faceA)
        self.mesh.add_face(faceB)

        faces = self.mesh.iter_faces()

        source_id = [0, 1]
        faces_id = [face.id for face in faces]

        self.assertItemsEqual(source_id, faces_id)

    def test_get_all_cells_iterator(self):
        """ Checks the cell iterators

        Checks that an interator over all
        the cells of the mesh is returned
        when the function iter_cells is called
        without arguments

        """

        pointsA = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]
        pointsB = [
            self.points[1],
            self.points[2],
            self.points[3],
            self.points[4]
            ]

        cellA = Cell(0, pointsA, 0)
        cellB = Cell(1, pointsB, 0)

        self.mesh.add_cell(cellA)
        self.mesh.add_cell(cellB)

        cells = self.mesh.iter_cells()

        source_id = [0, 1]
        cells_id = [cell.id for cell in cells]

        self.assertItemsEqual(source_id, cells_id)

    def test_get_subset_edges_iterator(self):
        """ Checks the edge iterator

        Checks that an interator over a subset of
        the edges of the mesh is returned
        when the function iter_edges is called
        selecting a list of id's

        """

        pointsA = [
            self.points[0],
            self.points[1]
            ]
        pointsB = [
            self.points[1],
            self.points[2]
            ]
        pointsC = [
            self.points[2],
            self.points[3]
            ]

        edgeA = Edge(0, pointsA, 0)
        edgeB = Edge(1, pointsB, 0)
        edgeC = Edge(2, pointsC, 0)

        self.mesh.add_edge(edgeA)
        self.mesh.add_edge(edgeB)
        self.mesh.add_edge(edgeC)

        edges = self.mesh.iter_edges([0, 2])

        source_id = [0, 2]
        edges_id = [edge.id for edge in edges]

        self.assertItemsEqual(source_id, edges_id)

    def test_get_subset_faces_iterator(self):
        """ Checks the face iterator

        Checks that an interator over a subset of
        the faces of the mesh is returned
        when the function iter_faces is called
        selecting a list of id's

        """

        pointsA = [
            self.points[0],
            self.points[1],
            self.points[2]
            ]
        pointsB = [
            self.points[1],
            self.points[2],
            self.points[3]
            ]
        pointsC = [
            self.points[2],
            self.points[3],
            self.points[4]
            ]

        faceA = Face(0, pointsA, 0)
        faceB = Face(1, pointsB, 0)
        faceC = Face(2, pointsC, 0)

        self.mesh.add_face(faceA)
        self.mesh.add_face(faceB)
        self.mesh.add_face(faceC)

        faces = self.mesh.iter_faces([0, 2])

        source_id = [0, 2]
        faces_id = [face.id for face in faces]

        self.assertItemsEqual(source_id, faces_id)

    def test_get_subset_cells_iterator(self):
        """ Checks the cell iterator

        Checks that an interator over a subset of
        the cells of the mesh is returned
        when the function iter_cells is called
        selecting a list of id's

        """

        pointsA = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]
        pointsB = [
            self.points[1],
            self.points[2],
            self.points[3],
            self.points[4]
            ]
        pointsC = [
            self.points[0],
            self.points[1],
            self.points[3],
            self.points[4]
            ]

        cellA = Cell(0, pointsA, 0)
        cellB = Cell(1, pointsB, 0)
        cellC = Cell(2, pointsC, 0)

        self.mesh.add_cell(cellA)
        self.mesh.add_cell(cellB)
        self.mesh.add_cell(cellC)

        cells = self.mesh.iter_cells([0, 2])

        source_id = [0, 2]
        cells_id = [cell.id for cell in cells]

        self.assertItemsEqual(source_id, cells_id)

if __name__ == '__main__':
    unittest.main()
