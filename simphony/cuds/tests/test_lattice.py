"""
    Testing module for lattice data classes.
"""
import unittest
from numpy.testing import assert_array_equal
from math import sqrt

from simphony.core.cuba import CUBA
from simphony.testing.abc_check_lattice import ABCCheckLattice
from simphony.cuds.lattice import (
    Lattice, LatticeNode, make_cubic_lattice, make_rectangular_lattice,
    make_square_lattice, make_orthorombicp_lattice, make_hexagonal_lattice)
from simphony.core.data_container import DataContainer


class LatticeNodeTestCase(unittest.TestCase):
    """Test case for LatticeNode class."""

    def test_construct_lattice_node_default(self):
        """Creation of a lattice node."""
        node = LatticeNode((0, 0, 0))

        self.assertIsInstance(node, LatticeNode,
                              "Error: not a LatticeNode!")
        self.assertEqual(node.index, (0, 0, 0))

    def test_construct_lattice_node_copy(self):
        """Creation of a lattice node (copy constructor)."""
        node_org = LatticeNode((0, 0, 1))
        node_org.data[CUBA.DENSITY] = 1.5
        node_org.data[CUBA.VELOCITY] = (0.2, -0.1, 0.0)

        node_new = LatticeNode((2, 3, 1), node_org.data)

        self.assertIsInstance(node_new, LatticeNode,
                              "Error: not a LatticeNode!")
        self.assertEqual(node_new.index, (2, 3, 1))
        self.assertEqual(node_new.data[CUBA.DENSITY], 1.5)
        self.assertEqual(node_new.data[CUBA.VELOCITY], (0.2, -0.1, 0.0))


class TestLattice(ABCCheckLattice, unittest.TestCase):

    def container_factory(self, name, type_, base_vect, size, origin):
        return Lattice(name, type_, base_vect, size, origin)

    def supported_cuba(self):
        return set(CUBA)

    def test_construct_lattice_make(self):
        """ Test creation of lattices using the factory functions.

        """

        hexag_lat = make_hexagonal_lattice('Lattice1', 0.1, (11, 21))
        square_lat = make_square_lattice('Lattice2', 0.2, (12, 22))
        rectang_lat = make_rectangular_lattice(
            'Lattice3', (0.3, 0.35), (13, 23))
        cubic_lat = make_cubic_lattice(
            'Lattice4', 0.4, (14, 24, 34), (4, 5, 6))
        orthop_lat = make_orthorombicp_lattice(
            'Lattice5', (0.5, 0.54, 0.58), (15, 25, 35), (7, 8, 9))

        self.assertIsInstance(hexag_lat, Lattice, "Error: not a Lattice!")
        self.assertIsInstance(square_lat, Lattice, "Error: not a Lattice!")
        self.assertIsInstance(rectang_lat, Lattice, "Error: not a Lattice!")
        self.assertIsInstance(cubic_lat, Lattice, "Error: not a Lattice!")
        self.assertIsInstance(orthop_lat, Lattice, "Error: not a Lattice!")

        self.assertEqual(hexag_lat.name, 'Lattice1')
        self.assertEqual(square_lat.name, 'Lattice2')
        self.assertEqual(rectang_lat.name, 'Lattice3')
        self.assertEqual(cubic_lat.name, 'Lattice4')
        self.assertEqual(orthop_lat.name, 'Lattice5')

        self.assertEqual(hexag_lat.type, 'Hexagonal')
        self.assertEqual(square_lat.type, 'Square')
        self.assertEqual(rectang_lat.type, 'Rectangular')
        self.assertEqual(cubic_lat.type, 'Cubic')
        self.assertEqual(orthop_lat.type, 'OrthorombicP')

        assert_array_equal(hexag_lat.size, (11, 21, 1))
        assert_array_equal(square_lat.size, (12, 22, 1))
        assert_array_equal(rectang_lat.size, (13, 23, 1))
        assert_array_equal(cubic_lat.size, (14, 24, 34))
        assert_array_equal(orthop_lat.size, (15, 25, 35))

        assert_array_equal(hexag_lat.origin, (0, 0, 0))
        assert_array_equal(square_lat.origin, (0, 0, 0))
        assert_array_equal(rectang_lat.origin, (0, 0, 0))
        assert_array_equal(cubic_lat.origin, (4, 5, 6))
        assert_array_equal(orthop_lat.origin, (7, 8, 9))

        assert_array_equal(hexag_lat.base_vect,
                           (0.5*0.1, 0.5*sqrt(3)*0.1, 0))
        assert_array_equal(square_lat.base_vect, (0.2, 0.2, 0))
        assert_array_equal(rectang_lat.base_vect, (0.3, 0.35, 0))
        assert_array_equal(cubic_lat.base_vect, (0.4, 0.4, 0.4))
        assert_array_equal(orthop_lat.base_vect, (0.5, 0.54, 0.58))

    def test_set_modify_data(self):
        """ Check that data can be retrieved and is consistent. Check that
        the internal data of the lattice cannot be modified outside the
        lattice class
        """
        lattice = self.container_factory('test_lat', 'Cubic',
                                         (1.0, 1.0, 1.0), (4, 3, 2),
                                         (0, 0, 0))
        org_data = DataContainer()

        org_data[CUBA.VELOCITY] = (0, 0, 0)

        lattice.data = org_data
        ret_data = lattice.data

        self.assertEqual(org_data, ret_data)
        self.assertIsNot(org_data, ret_data)

        org_data = DataContainer()

        org_data[CUBA.VELOCITY] = (0, 0, 0)

        lattice.data = org_data
        mod_data = lattice.data

        mod_data[CUBA.VELOCITY] = (1, 1, 1)

        ret_data = lattice.data

        self.assertEqual(org_data, ret_data)
        self.assertIsNot(org_data, ret_data)


if __name__ == '__main__':
    unittest.main()
