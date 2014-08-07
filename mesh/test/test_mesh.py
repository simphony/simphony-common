import unittest
import mesh

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.mesh   = mesh.Mesh();
        self.points = [mesh.Point(0, (0.0, 0.0, 0.0), 0),
                       mesh.Point(1, (1.0, 0.0, 0.0), 0),
                       mesh.Point(2, (0.0, 1.0, 0.0), 0),
                       mesh.Point(3, (0.0, 0.0, 1.0), 0)
                      ]

    def test_emtpy(self):
        self.assertFalse(self.mesh.has_edges())
        self.assertFalse(self.mesh.has_faces())
        self.assertFalse(self.mesh.has_cells())

    def test_add_edge(self):
        edge = mesh.Edge(0,[self.points[0], self.points[1]],0)

        self.mesh.add_edge(edge)

        self.assertTrue(self.mesh.has_edges())
        self.assertFalse(self.mesh.has_faces())
        self.assertFalse(self.mesh.has_cells())

    def test_add_face(self):
        face = mesh.Face(0,[self.points[0], self.points[1], self.points[2]],0)

        self.mesh.add_face(face)

        self.assertFalse(self.mesh.has_edges())
        self.assertTrue(self.mesh.has_faces())
        self.assertFalse(self.mesh.has_cells())

    def test_add_cell(self):
        cell = mesh.Cell(0,[self.points[0], self.points[1], self.points[2], self.points[3]],0)

        self.mesh.add_cell(cell)

        self.assertFalse(self.mesh.has_edges())
        self.assertFalse(self.mesh.has_faces())
        self.assertTrue(self.mesh.has_cells())

if __name__ == '__main__':
    unittest.main()
