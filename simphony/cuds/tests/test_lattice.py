"""
    Testing module for lattice data classes.
"""
import unittest
from numpy.testing import assert_array_equal

from simphony.core.cuba import CUBA
from simphony.testing.abc_check_lattice import (
    CheckLatticeContainer, CheckLatticeNodeOperations,
    CheckLatticeNodeCoordinates)
from simphony.cuds.lattice import (Lattice, LatticeNode,
    make_cubic_lattice, make_body_centered_cubic_lattice,
    make_face_centered_cubic_lattice, make_rhombohedral_lattice,
    make_hexagonal_lattice, make_tetragonal_lattice,
    make_body_centered_tetragonal_lattice, make_orthorhombic_lattice,
    make_body_centered_orthorhombic_lattice,
    make_face_centered_orthorhombic_lattice,
    make_base_centered_orthorhombic_lattice, make_monoclinic_lattice,
    make_base_centered_monoclinic_lattice, make_triclinic_lattice)
from simphony.cuds.primitive_cell import BravaisLattice


class LatticeNodeTestCase(unittest.TestCase):
    """Test case for LatticeNode class."""

    def test_construct_lattice_node_default(self):
        """Creation of a lattice node."""
        node = LatticeNode((0, 0, 0))

        self.assertIsInstance(node, LatticeNode)
        self.assertEqual(node.index, (0, 0, 0))

    def test_construct_lattice_node_copy(self):
        """Creation of a lattice node (copy constructor)."""
        node_org = LatticeNode((0, 0, 1))
        node_org.data[CUBA.DENSITY] = 1.5
        node_org.data[CUBA.VELOCITY] = (0.2, -0.1, 0.0)

        node_new = LatticeNode((2, 3, 1), node_org.data)

        self.assertIsInstance(node_new, LatticeNode)
        self.assertEqual(node_new.index, (2, 3, 1))
        self.assertEqual(node_new.data[CUBA.DENSITY], 1.5)
        self.assertEqual(node_new.data[CUBA.VELOCITY], (0.2, -0.1, 0.0))


class TestLatticeNodeOperations(CheckLatticeNodeOperations, unittest.TestCase):

    def container_factory(self, name, prim_cell, size, origin):
        return Lattice(name, prim_cell, size, origin)

    def supported_cuba(self):
        return set(CUBA)


class TestLatticeNodeCoordinates(
        CheckLatticeNodeCoordinates, unittest.TestCase):

    def container_factory(self, name, prim_cell, size, origin):
        return Lattice(name, prim_cell, size, origin)

    def supported_cuba(self):
        return set(CUBA)


class TestLatticeContainer(CheckLatticeContainer, unittest.TestCase):

    def container_factory(self, name, prim_cell, size, origin):
        return Lattice(name, prim_cell, size, origin)

    def supported_cuba(self):
        return set(CUBA)


class TestLatticeFactories(unittest.TestCase):

    def setUp(self):
        self.a, self.b, self.c = 0.4, 0.9, 1.4
        self.alpha, self.beta, self.gamma =  0.7, 0.64, 1.2

    def test_make_cubic_lattice(self):
        lattice = make_cubic_lattice('Lattice0',
                    self.a, (14, 4, 5), (4, 5, 6))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice0')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.CUBIC)
        assert_array_equal(lattice.size, (14, 4, 5))
        assert_array_equal(lattice.origin, (4, 5, 6))

    def test_make_body_centered_cubic_lattice(self):
        lattice = make_body_centered_cubic_lattice('Lattice1',
                    self.a, (3, 3, 3))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice1')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.BODY_CENTERED_CUBIC)
        assert_array_equal(lattice.size, (3, 3, 3))
        assert_array_equal(lattice.origin, (0, 0, 0))

    def test_make_face_centered_cubic_lattice(self):
        lattice = make_face_centered_cubic_lattice('Lattice2',
                    self.a, (6, 7, 4))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice2')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.FACE_CENTERED_CUBIC)
        assert_array_equal(lattice.size, (6, 7, 4))
        assert_array_equal(lattice.origin, (0, 0, 0))

    def test_make_rhombohedral_lattice(self):
        lattice = make_rhombohedral_lattice('Lattice3',
                    self.a, self.alpha, (10, 2, 4))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice3')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.RHOMBOHEDRAL)
        assert_array_equal(lattice.size, (10, 2, 4))
        assert_array_equal(lattice.origin, (0, 0, 0))

    def test_make_tetragonal_lattice(self):
        lattice = make_tetragonal_lattice('Lattice4',
                    self.a, self.c, (3, 4, 3))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice4')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.TETRAGONAL)
        assert_array_equal(lattice.size, (3, 4, 3))
        assert_array_equal(lattice.origin, (0, 0, 0))

    def test_make_body_centered_tetragonal_lattice(self):
        lattice = make_body_centered_tetragonal_lattice('Lattice5',
                    self.a, self.c, (4, 4, 4))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice5')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.BODY_CENTERED_TETRAGONAL)
        assert_array_equal(lattice.size, (4, 4, 4))
        assert_array_equal(lattice.origin, (0, 0, 0))

    def test_make_hexagonal_lattice(self):
        lattice = make_hexagonal_lattice('Lattice6',
                    self.a, self.c, (5, 5, 5))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice6')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.HEXAGONAL)
        assert_array_equal(lattice.size, (5, 5, 5))
        assert_array_equal(lattice.origin, (0, 0, 0))

    def test_make_orthorhombic_lattice(self):
        lattice = make_orthorhombic_lattice('Lattice7',
                    (self.a, self.b, self.c), (6, 2, 2))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice7')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.ORTHORHOMBIC)
        assert_array_equal(lattice.size, (6, 2, 2))
        assert_array_equal(lattice.origin, (0, 0, 0))

    def test_make_body_centered_orthorhombic_lattice(self):
        lattice = make_body_centered_orthorhombic_lattice('Lattice8',
                    (self.a, self.b, self.c), (3, 2, 9))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice8')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.BODY_CENTERED_ORTHORHOMBIC)
        assert_array_equal(lattice.size, (3, 2, 9))
        assert_array_equal(lattice.origin, (0, 0, 0))

    def test_make_face_centered_orthorhombic_lattice(self):
        lattice = make_face_centered_orthorhombic_lattice('Lattice9',
                    (self.a, self.b, self.c), (7, 4, 8))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice9')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.FACE_CENTERED_ORTHORHOMBIC)
        assert_array_equal(lattice.size, (7, 4, 8))
        assert_array_equal(lattice.origin, (0, 0, 0))

    def test_make_base_centered_orthorhombic_lattice(self):
        lattice = make_base_centered_orthorhombic_lattice('Lattice10',
                    (self.a, self.b, self.c), (6, 6, 6))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice10')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.BASE_CENTERED_ORTHORHOMBIC)
        assert_array_equal(lattice.size, (6, 6, 6))
        assert_array_equal(lattice.origin, (0, 0, 0))

    def test_make_monoclinic_lattice(self):
        lattice = make_monoclinic_lattice('Lattice11',
                    (self.a, self.b, self.c), self.beta, (7, 3, 2))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice11')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.MONOCLINIC)
        assert_array_equal(lattice.size, (7, 3, 2))
        assert_array_equal(lattice.origin, (0, 0, 0))

    def test_make_base_centered_monoclinic_lattice(self):
        lattice = make_base_centered_monoclinic_lattice('Lattice12',
                    (self.a, self.b, self.c), self.beta, (5, 3, 4))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice12')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.BASE_CENTERED_MONOCLINIC)
        assert_array_equal(lattice.size, (5, 3, 4))
        assert_array_equal(lattice.origin, (0, 0, 0))

    def test_make_triclinic_lattice(self):
        lattice = make_triclinic_lattice('Lattice13',
                    (self.a, self.b, self.c),
                    (self.alpha, self.beta, self.gamma), (4, 5, 6))
        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice13')
        self.assertEqual(lattice.prim_cell.bravais_lattice,
                         BravaisLattice.TRICLINIC)
        assert_array_equal(lattice.size, (4, 5, 6))
        assert_array_equal(lattice.origin, (0, 0, 0))


if __name__ == '__main__':
    unittest.main()
