import unittest
import cuds.mesh

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.mesh   = cuds.mesh.Mesh();
        self.points = [cuds.mesh.Point(0, (0.0, 0.0, 0.0), 0),
                       cuds.mesh.Point(1, (1.0, 0.0, 0.0), 0),
                       cuds.mesh.Point(2, (0.0, 1.0, 0.0), 0),
                       cuds.mesh.Point(3, (0.0, 0.0, 1.0), 0)
                      ]

    def test_emtpy(self):
        self.assertFalse(self.mesh.has_edges())
        self.assertFalse(self.mesh.has_faces())
        self.assertFalse(self.mesh.has_cells())

    def test_add_edge(self):
        edge = cuds.mesh.Edge(0,[self.points[0], self.points[1]],0)

        self.mesh.add_edge(edge)

        self.assertTrue(self.mesh.has_edges())
        self.assertFalse(self.mesh.has_faces())
        self.assertFalse(self.mesh.has_cells())

    def test_add_face(self):
        face = cuds.mesh.Face(0,[self.points[0], self.points[1], self.points[2]],0)

        self.mesh.add_face(face)

        self.assertFalse(self.mesh.has_edges())
        self.assertTrue(self.mesh.has_faces())
        self.assertFalse(self.mesh.has_cells())

    def test_add_cell(self):
        cell = cuds.mesh.Cell(0,[self.points[0], self.points[1], self.points[2], self.points[3]],0)

        self.mesh.add_cell(cell)

        self.assertFalse(self.mesh.has_edges())
        self.assertFalse(self.mesh.has_faces())
        self.assertTrue(self.mesh.has_cells())

if __name__ == '__main__':
    unittest.main()
