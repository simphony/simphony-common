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
# import simphony.core.data_container as dc
# from simphony.core.cuba import CUBA


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        """ Creates an empty mesh to perform the tests

        Creates an empty mesh and and a set of points
        to tests all the mesh methods

        """
        self.mesh = Mesh()
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

        pids = []

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        self.assertIsNotNone(self.mesh.get_point(pids[0]))

    def test_add_edge(self):
        """ Check that an edge can be added correctly

        """

        points = [
            self.points[0],
            self.points[1]
            ]

        pids = []
        eids = []

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        edge = Edge(pids[0:2])

        eid = self.mesh.add_edge(edge)
        eids.append(eid)

        self.assertIsNotNone(self.mesh.get_edge(eids[0]))

    def test_add_face(self):
        """ Check that a face can be added correctly

        """

        points = [
            self.points[0],
            self.points[1],
            self.points[2]
            ]

        pids = []
        fids = []

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        face = Face(pids[0:3])

        fid = self.mesh.add_face(face)
        fids.append(fid)

        self.assertIsNotNone(self.mesh.get_face(fids[0]))

    def test_add_cell(self):
        """ Check that a cell can be added correctly

        """

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        pids = []
        cids = []

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        cell = Cell(pids[0:4])

        cid = self.mesh.add_cell(cell)
        cids.append(cid)

        self.assertIsNotNone(self.mesh.get_cell(cids[0]))

    def test_non_emtpy_edges(self):
        """ Checks that the list of edges is not empty

        """

        points = [
            self.points[0],
            self.points[1]
            ]

        pids = []

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        edge = Edge(pids[0:2])

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

        pids = []

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        face = Face(pids[0:3])

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

        pids = []

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        cell = Cell(pids[0:4])

        self.mesh.add_cell(cell)

        self.assertTrue(self.mesh.has_cells())

    def test_get_point(self):
        """ Check that a point can be retrieved correctly

        """

        pids = []

        points = [self.points[0]]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        point_ret = self.mesh.get_point(pids[0])

        self.assertTrue(isinstance(point_ret, Point))
        self.assertEqual(pids[0], point_ret.id)

    def test_get_edge(self):
        """ Check that an edge can be retrieved correctly

        """

        pids = []
        eids = []

        points = [
            self.points[0],
            self.points[1]
            ]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        edge = Edge(pids[:])

        eid = self.mesh.add_edge(edge)
        eids.append(eid)

        edge_ret = self.mesh.get_edge(eids[0])

        self.assertTrue(isinstance(edge_ret, Edge))
        self.assertEqual(eids[0], edge_ret.id)

    def test_get_face(self):
        """ Check that a face can be retrieved correctly

        """

        pids = []
        fids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2]
            ]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        face = Face(pids[:])

        fid = self.mesh.add_face(face)
        fids.append(fid)

        face_ret = self.mesh.get_face(fids[0])

        self.assertTrue(isinstance(face_ret, Face))
        self.assertEqual(fids[0], face_ret.id)

    def test_get_cell(self):
        """ Check that a cell can be retrieved correctly

        """

        pids = []
        cids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        cell = Cell(pids[:])

        cid = self.mesh.add_cell(cell)
        cids.append(cid)

        cell_ret = self.mesh.get_cell(cids[0])

        self.assertTrue(isinstance(cell_ret, Cell))
        self.assertEqual(cids[0], cell_ret.id)

    def test_get_all_edges_iterator(self):
        """ Checks the edge iterator

        Checks that an interator over all
        the edges of the mesh is returned
        when the function iter_edges is called
        without arguments

        """

        pids = []
        eids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2]
            ]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        edges = [
            Edge(pids[0:2]),
            Edge(pids[1:3])
        ]

        for edge in edges:
            eid = self.mesh.add_edge(edge)
            eids.append(eid)

        iedges = self.mesh.iter_edges()

        iedges_id = [edge.id for edge in iedges]

        self.assertItemsEqual(iedges_id, eids)

    def test_get_all_faces_iterator(self):
        """ Checks the face iterator

        Checks that an interator over all
        the faces of the mesh is returned
        when the function iter_faces is called
        without arguments

        """

        pids = []
        fids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        faces = [
            Face(pids[0:3]),
            Face(pids[1:4])
        ]

        for face in faces:
            fid = self.mesh.add_face(face)
            fids.append(fid)

        ifaces = self.mesh.iter_faces()

        ifaces_id = [face.id for face in ifaces]

        self.assertItemsEqual(fids, ifaces_id)

    def test_get_all_cells_iterator(self):
        """ Checks the cell iterators

        Checks that an interator over all
        the cells of the mesh is returned
        when the function iter_cells is called
        without arguments

        """

        pids = []
        cids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3],
            self.points[4]
            ]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        cells = [
            Cell(pids[0:4]),
            Cell(pids[1:5])
            ]

        for cell in cells:
            cid = self.mesh.add_cell(cell)
            cids.append(cid)

        icells = self.mesh.iter_cells()

        icells_id = [cell.id for cell in icells]

        self.assertItemsEqual(icells_id, cids)

    def test_get_subset_edges_iterator(self):
        """ Checks the edge iterator

        Checks that an interator over a subset of
        the edges of the mesh is returned
        when the function iter_edges is called
        selecting a list of id's

        """

        pids = []
        eids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        edges = [
            Edge(pids[0:2]),
            Edge(pids[2:3]),
            Edge(pids[3:4])
            ]

        for edge in edges:
            eid = self.mesh.add_edge(edge)
            eids.append(eid)

        iedges = self.mesh.iter_edges([eids[0], eids[2]])

        source_id = [eids[0], eids[2]]
        iedges_id = [edge.id for edge in iedges]

        self.assertItemsEqual(source_id, iedges_id)

    def test_get_subset_faces_iterator(self):
        """ Checks the face iterator

        Checks that an interator over a subset of
        the faces of the mesh is returned
        when the function iter_faces is called
        selecting a list of id's

        """

        pids = []
        fids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3],
            self.points[4]
            ]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        faces = [
            Face(pids[0:3]),
            Face(pids[1:4]),
            Face(pids[2:5])
            ]

        for face in faces:
            fid = self.mesh.add_face(face)
            fids.append(fid)

        ifaces = self.mesh.iter_faces([fids[0], fids[2]])

        source_id = [fids[0], fids[2]]
        ifaces_id = [face.id for face in ifaces]

        self.assertItemsEqual(source_id, ifaces_id)

    def test_get_subset_cells_iterator(self):
        """ Checks the cell iterator

        Checks that an interator over a subset of
        the cells of the mesh is returned
        when the function iter_cells is called
        selecting a list of id's

        """

        pids = []
        cids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3],
            self.points[4],
            self.points[5]
            ]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        cells = [
            Cell(pids[0:4]),
            Cell(pids[1:5]),
            Cell(pids[2:6])
            ]

        for cell in cells:
            cid = self.mesh.add_cell(cell)
            cids.append(cid)

        icells = self.mesh.iter_cells([cids[0], cids[2]])

        source_id = [cids[0], cids[2]]
        icells_id = [cell.id for cell in icells]

        self.assertItemsEqual(source_id, icells_id)

    def test_update_point(self):
        pids = []

        points = [
            self.points[0],
            ]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        point_ret = self.mesh.get_point(pids[0])
        point_ret.coordinates = [-1.0 -1.0 -1.0]
        self.mesh.update_point(point_ret)

        point_upd = self.mesh.get_point(pids[0])

        self.assertItemsEqual(point_upd.coordinates, point_ret.coordinates)

    def test_update_edge(self):
        """ Check that an edge can be updated correctly

        """

        pids = []
        eids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2]
            ]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        edge = Edge(pids[0:2])

        eid = self.mesh.add_edge(edge)
        eids.append(eid)

        edge_ret = self.mesh.get_edge(eids[0])
        edge_ret.points[1] = pids[2]
        self.mesh.update_edge(edge_ret)

        edge_upd = self.mesh.get_edge(eids[0])

        self.assertItemsEqual(edge_upd.points, edge_ret.points)

    def test_update_face(self):
        """ Check that a face can be updated correctly

        """

        pids = []
        fids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3]
            ]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        face = Face(pids[0:3])

        fid = self.mesh.add_face(face)
        fids.append(fid)

        face_ret = self.mesh.get_face(fids[0])
        face_ret.points[2] = pids[3]
        self.mesh.update_face(face_ret)

        face_upd = self.mesh.get_face(fids[0])

        self.assertItemsEqual(face_upd.points, face_ret.points)

    def test_update_cell(self):
        """ Check that a cell can be updated correctly

        """

        pids = []
        cids = []

        points = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3],
            self.points[4]
            ]

        for point in points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        cell = Cell(pids[0:4])

        cid = self.mesh.add_cell(cell)
        cids.append(cid)

        cell_ret = self.mesh.get_cell(cids[0])
        cell_ret.points[3] = pids[4]
        self.mesh.update_cell(cell_ret)

        cell_upd = self.mesh.get_cell(cids[0])

        self.assertItemsEqual(cell_upd.points, cell_ret.points)

if __name__ == '__main__':
    unittest.main()
