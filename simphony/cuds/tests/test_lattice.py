"""
    Testing module for lattice data classes.
"""
import unittest
from numpy.testing import assert_array_equal
from math import sqrt

from simphony.core.cuba import CUBA
from simphony.testing.abc_check_lattice import (
    CheckLatticeProperties, CheckLatticeNodeOperations,
    CheckLatticeNodeCoordinates)
from simphony.cuds.lattice import (
    Lattice, LatticeNode, make_cubic_lattice, make_rectangular_lattice,
    make_square_lattice, make_orthorombicp_lattice, make_hexagonal_lattice)


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

    def container_factory(self, name, type_, base_vect, size, origin):
        return Lattice(name, type_, base_vect, size, origin)

    def supported_cuba(self):
        return set(CUBA)


class TestLatticeNodeCoordinates(
        CheckLatticeNodeCoordinates, unittest.TestCase):

    def container_factory(self, name, type_, base_vect, size, origin):
        return Lattice(name, type_, base_vect, size, origin)

    def supported_cuba(self):
        return set(CUBA)

    @unittest.skip('Hexagonal coordinates are not supported yet')
    def test_get_coordinate_hexagonal(self):
        pass


class TestLatticeProperties(CheckLatticeProperties, unittest.TestCase):

    def container_factory(self, name, type_, base_vect, size, origin):
        return Lattice(name, type_, base_vect, size, origin)

    def supported_cuba(self):
        return set(CUBA)


class TestLatticeFactories(unittest.TestCase):

    def test_make_hexagonal(self):
        lattice = make_hexagonal_lattice('Lattice1', 0.1, (11, 21))

        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice1')
        self.assertEqual(lattice.type, 'Hexagonal')
        assert_array_equal(lattice.size, (11, 21, 1))
        assert_array_equal(lattice.origin, (0, 0, 0))
        assert_array_equal(lattice.base_vect,
                           (0.5*0.1, 0.5*sqrt(3)*0.1, 0))

    def test_make_square(self):
        lattice = make_square_lattice('Lattice2', 0.2, (12, 22))

        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice2')
        self.assertEqual(lattice.type, 'Square')
        assert_array_equal(lattice.size, (12, 22, 1))
        assert_array_equal(lattice.origin, (0, 0, 0))
        assert_array_equal(lattice.base_vect, (0.2, 0.2, 0))

    def test_make_cubic(self):
        lattice = make_cubic_lattice('Lattice4', 0.4, (14, 24, 34), (4, 5, 6))

        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice4')
        self.assertEqual(lattice.type, 'Cubic')
        assert_array_equal(lattice.size, (14, 24, 34))
        assert_array_equal(lattice.origin, (4, 5, 6))
        assert_array_equal(lattice.base_vect, (0.4, 0.4, 0.4))

    def test_make_rectangular(self):
        lattice = make_rectangular_lattice('Lattice3', (0.3, 0.35), (13, 23))

        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice3')
        self.assertEqual(lattice.type, 'Rectangular')
        assert_array_equal(lattice.size, (13, 23, 1))
        assert_array_equal(lattice.origin, (0, 0, 0))
        assert_array_equal(lattice.base_vect, (0.3, 0.35, 0))

    def test_orthorombicp_lattice(self):
        lattice = make_orthorombicp_lattice(
            'Lattice5', (0.5, 0.54, 0.58), (15, 25, 35), (7, 8, 9))

        self.assertIsInstance(lattice, Lattice)
        self.assertEqual(lattice.name, 'Lattice5')
        self.assertEqual(lattice.type, 'OrthorombicP')
        assert_array_equal(lattice.size, (15, 25, 35))
        assert_array_equal(lattice.origin, (7, 8, 9))
        assert_array_equal(lattice.base_vect, (0.5, 0.54, 0.58))


if __name__ == '__main__':
    unittest.main()
