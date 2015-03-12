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

from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        """ Creates an empty mesh to perform the tests

        Creates an empty mesh and and a set of points
        to tests all the mesh methods

        """
        self.mesh = Mesh(name="foo")
        self.points = [
            Point((0.0, 0.0, 0.0)),
            Point((1.0, 0.0, 0.0)),
            Point((0.0, 1.0, 0.0)),
            Point((0.0, 0.0, 1.0)),
            Point((1.0, 0.0, 1.0)),
            Point((0.0, 1.0, 1.0))
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

        points = [
            self.points[0]
            ]

        puuids = []

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        self.assertIsNotNone(self.mesh.get_point(puuids[0]))

    def test_add_edge(self):
        """ Check that an edge can be added correctly

        """

        points = [
            self.points[0],
            self.points[1]
            ]

        puuids = []
        euuids = []

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        edge = Edge(puuids[0:2])

        euuid = self.mesh.add_edge(edge)
        euuids.append(euuid)

        self.assertIsNotNone(self.mesh.get_edge(euuids[0]))

    def test_add_face(self):
        """ Check that a face can be added correctly

        """

        points = [
            self.points[0],
            self.points[1],
            self.points[2]
            ]

        puuids = []
        fuuids = []

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        face = Face(puuids[0:3])

        fuuid = self.mesh.add_face(face)
        fuuids.append(fuuid)

        self.assertIsNotNone(self.mesh.get_face(fuuids[0]))

    def test_add_cell(self):
        """ Check that a cell can be added correctly

        """

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        puuids = []
        cuuids = []

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        cell = Cell(puuids[0:4])

        cuuid = self.mesh.add_cell(cell)
        cuuids.append(cuuid)

        self.assertIsNotNone(self.mesh.get_cell(cuuids[0]))

    def test_non_emtpy_edges(self):
        """ Checks that the list of edges is not empty

        """

        points = [
            self.points[0],
            self.points[1]
            ]

        puuids = []

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        edge = Edge(puuids[0:2])

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

        puuids = []

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        face = Face(puuids[0:3])

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

        puuids = []

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        cell = Cell(puuids[0:4])

        self.mesh.add_cell(cell)

        self.assertTrue(self.mesh.has_cells())

    def test_get_point(self):
        """ Check that a point can be retrieved correctly

        """

        puuids = []

        points = [self.points[0]]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        point_ret = self.mesh.get_point(puuids[0])

        self.assertTrue(isinstance(point_ret, Point))
        self.assertEqual(puuids[0], point_ret.uid)

    def test_get_edge(self):
        """ Check that an edge can be retrieved correctly

        """

        puuids = []
        euuids = []

        points = [
            self.points[0],
            self.points[1]
            ]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        edge = Edge(puuids[:])

        euuid = self.mesh.add_edge(edge)
        euuids.append(euuid)

        edge_ret = self.mesh.get_edge(euuids[0])

        self.assertTrue(isinstance(edge_ret, Edge))
        self.assertEqual(euuids[0], edge_ret.uid)

    def test_get_face(self):
        """ Check that a face can be retrieved correctly

        """

        puuids = []
        fuuids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2]
            ]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        face = Face(puuids[:])

        fuuid = self.mesh.add_face(face)
        fuuids.append(fuuid)

        face_ret = self.mesh.get_face(fuuids[0])

        self.assertTrue(isinstance(face_ret, Face))
        self.assertEqual(fuuids[0], face_ret.uid)

    def test_get_cell(self):
        """ Check that a cell can be retrieved correctly

        """

        puuids = []
        cuuids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        cell = Cell(puuids[:])

        cuuid = self.mesh.add_cell(cell)
        cuuids.append(cuuid)

        cell_ret = self.mesh.get_cell(cuuids[0])

        self.assertTrue(isinstance(cell_ret, Cell))
        self.assertEqual(cuuids[0], cell_ret.uid)

    def test_get_all_edges_iterator(self):
        """ Checks the edge iterator

        Checks that an interator over all
        the edges of the mesh is returned
        when the function iter_edges is called
        without arguments

        """

        puuids = []
        euuids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2]
            ]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        edges = [
            Edge(puuids[0:2]),
            Edge(puuids[1:3])
        ]

        for edge in edges:
            euuid = self.mesh.add_edge(edge)
            euuids.append(euuid)

        iedges = self.mesh.iter_edges()

        iedges_id = [edge.uid for edge in iedges]

        self.assertItemsEqual(iedges_id, euuids)

    def test_get_all_faces_iterator(self):
        """ Checks the face iterator

        Checks that an interator over all
        the faces of the mesh is returned
        when the function iter_faces is called
        without arguments

        """

        puuids = []
        fuuids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        faces = [
            Face(puuids[0:3]),
            Face(puuids[1:4])
        ]

        for face in faces:
            fuuid = self.mesh.add_face(face)
            fuuids.append(fuuid)

        ifaces = self.mesh.iter_faces()

        ifaces_id = [face.uid for face in ifaces]

        self.assertItemsEqual(fuuids, ifaces_id)

    def test_get_all_cells_iterator(self):
        """ Checks the cell iterators

        Checks that an interator over all
        the cells of the mesh is returned
        when the function iter_cells is called
        without arguments

        """

        puuids = []
        cuuids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3],
            self.points[4]
            ]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        cells = [
            Cell(puuids[0:4]),
            Cell(puuids[1:5])
            ]

        for cell in cells:
            cuuid = self.mesh.add_cell(cell)
            cuuids.append(cuuid)

        icells = self.mesh.iter_cells()

        icells_id = [cell.uid for cell in icells]

        self.assertItemsEqual(icells_id, cuuids)

    def test_get_subset_edges_iterator(self):
        """ Checks the edge iterator

        Checks that an interator over a subset of
        the edges of the mesh is returned
        when the function iter_edges is called
        selecting a list of uuid's

        """

        puuids = []
        euuids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        edges = [
            Edge(puuids[0:2]),
            Edge(puuids[2:3]),
            Edge(puuids[3:4])
            ]

        for edge in edges:
            euuid = self.mesh.add_edge(edge)
            euuids.append(euuid)

        iedges = self.mesh.iter_edges([euuids[0], euuids[2]])

        source_id = [euuids[0], euuids[2]]
        iedges_id = [edge.uid for edge in iedges]

        self.assertItemsEqual(source_id, iedges_id)

    def test_get_subset_faces_iterator(self):
        """ Checks the face iterator

        Checks that an interator over a subset of
        the faces of the mesh is returned
        when the function iter_faces is called
        selecting a list of uuid's

        """

        puuids = []
        fuuids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3],
            self.points[4]
            ]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        faces = [
            Face(puuids[0:3]),
            Face(puuids[1:4]),
            Face(puuids[2:5])
            ]

        for face in faces:
            fuuid = self.mesh.add_face(face)
            fuuids.append(fuuid)

        ifaces = self.mesh.iter_faces([fuuids[0], fuuids[2]])

        source_id = [fuuids[0], fuuids[2]]
        ifaces_id = [face.uid for face in ifaces]

        self.assertItemsEqual(source_id, ifaces_id)

    def test_get_subset_cells_iterator(self):
        """ Checks the cell iterator

        Checks that an interator over a subset of
        the cells of the mesh is returned
        when the function iter_cells is called
        selecting a list of uuid's

        """

        puuids = []
        cuuids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3],
            self.points[4],
            self.points[5]
            ]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        cells = [
            Cell(puuids[0:4]),
            Cell(puuids[1:5]),
            Cell(puuids[2:6])
            ]

        for cell in cells:
            cuuid = self.mesh.add_cell(cell)
            cuuids.append(cuuid)

        icells = self.mesh.iter_cells([cuuids[0], cuuids[2]])

        source_id = [cuuids[0], cuuids[2]]
        icells_id = [cell.uid for cell in icells]

        self.assertItemsEqual(source_id, icells_id)

    def test_update_point(self):
        """ Check that a point can be updated correctly

        """

        puuids = []

        points = [
            self.points[0],
            ]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        point_ret = self.mesh.get_point(puuids[0])
        point_ret.coordinates = [-1.0, -1.0, -1.0]
        self.mesh.update_point(point_ret)

        point_upd = self.mesh.get_point(puuids[0])

        self.assertItemsEqual(point_upd.coordinates, point_ret.coordinates)

    def test_update_edge(self):
        """ Check that an edge can be updated correctly

        """

        puuids = []
        euuids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2]
            ]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        edge = Edge(puuids[0:2])

        euuid = self.mesh.add_edge(edge)
        euuids.append(euuid)

        edge_ret = self.mesh.get_edge(euuids[0])
        edge_ret.points[1] = puuids[2]
        self.mesh.update_edge(edge_ret)

        edge_upd = self.mesh.get_edge(euuids[0])

        self.assertItemsEqual(edge_upd.points, edge_ret.points)

    def test_update_face(self):
        """ Check that a face can be updated correctly

        """

        puuids = []
        fuuids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        face = Face(puuids[0:3])

        fuuid = self.mesh.add_face(face)
        fuuids.append(fuuid)

        face_ret = self.mesh.get_face(fuuids[0])
        face_ret.points[2] = puuids[3]
        self.mesh.update_face(face_ret)

        face_upd = self.mesh.get_face(fuuids[0])

        self.assertItemsEqual(face_upd.points, face_ret.points)

    def test_update_cell(self):
        """ Check that a cell can be updated correctly

        """

        puuids = []
        cuuids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3],
            self.points[4]
            ]

        for point in points:
            puuid = self.mesh.add_point(point)
            puuids.append(puuid)

        cell = Cell(puuids[0:4])

        cuuid = self.mesh.add_cell(cell)
        cuuids.append(cuuid)

        cell_ret = self.mesh.get_cell(cuuids[0])
        cell_ret.points[3] = puuids[4]
        self.mesh.update_cell(cell_ret)

        cell_upd = self.mesh.get_cell(cuuids[0])

        self.assertItemsEqual(cell_upd.points, cell_ret.points)

    def test_set_data(self):
        """ Check that data can be retrieved

        """

        org_data = DataContainer()

        org_data[CUBA.VELOCITY] = (0, 0, 0)

        self.mesh.data = org_data
        ret_data = self.mesh.data

        self.assertItemsEqual(org_data, ret_data)

    def test_modify_data(self):
        """ Check that data is consistent

        Check that the internal data of the mesh cannot be modified
        outise the mesh class

        """

        org_data = DataContainer()

        org_data[CUBA.VELOCITY] = (0, 0, 0)

        self.mesh.data = org_data
        mod_data = self.mesh.data

        mod_data[CUBA.VELOCITY] = (0, 0, 0)

        ret_data = self.mesh.data

        self.assertItemsEqual(org_data, ret_data)

if __name__ == '__main__':
    unittest.main()
