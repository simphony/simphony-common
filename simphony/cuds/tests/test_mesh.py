""" test_mesh module

This module contains the unitary tests for the
mesh module functionalities

"""
import unittest
import cuds.mesh


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        """ Creates an empty mesh to perform the tests

        Creates an empty mesh and and a set of points
        to tests all the mesh methods

        """
        self.mesh = cuds.mesh.Mesh()
        self.points = [cuds.mesh.Point(0, (0.0, 0.0, 0.0), 0),
                       cuds.mesh.Point(1, (1.0, 0.0, 0.0), 0),
                       cuds.mesh.Point(2, (0.0, 1.0, 0.0), 0),
                       cuds.mesh.Point(3, (0.0, 0.0, 1.0), 0),
                       cuds.mesh.Point(4, (1.0, 0.0, 1.0), 0)
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

    def test_non_emtpy_edges(self):
        """ Checks that the list of edges is not empty

        """

        points = [
            self.points[0],
            self.points[1]
            ]

        edge = cuds.mesh.Edge(0, points, 0)

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

        face = cuds.mesh.Face(0, points, 0)

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

        cell = cuds.mesh.Cell(0, points, 0)

        self.mesh.add_cell(cell)
        self.assertTrue(self.mesh.has_cells())

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

        edgeA = cuds.mesh.Edge(0, pointsA, 0)
        edgeB = cuds.mesh.Edge(1, pointsB, 0)

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

        faceA = cuds.mesh.Face(0, pointsA, 0)
        faceB = cuds.mesh.Face(1, pointsB, 0)

        self.mesh.add_face(faceA)
        self.mesh.add_face(faceB)

        faces = self.mesh.iter_face()

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

        cellA = cuds.mesh.Cell(0, pointsA, 0)
        cellB = cuds.mesh.Cell(1, pointsB, 0)

        self.mesh.add_cell(cellA)
        self.mesh.add_cell(cellB)

        cells = self.mesh.iter_cell()

        source_id = [0, 1]
        cells_id = [cell.id for cell in cells]

        self.assertItemsEqual(source_id, cells_id)

if __name__ == '__main__':
    unittest.main()
