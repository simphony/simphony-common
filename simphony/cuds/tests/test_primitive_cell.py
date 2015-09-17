"""
    Testing module for PrimitiveCell class.
"""
import unittest

from numpy.testing import assert_array_equal
import numpy as np
from simphony.cuds.primitive_cell import PrimitiveCell, BravaisLattice


class TestPrimitiveCell(unittest.TestCase):

    def setUp(self):
        self.a, self.b, self.c = 0.4, 0.9, 1.4
        self.alpha, self.beta, self.gamma = 0.6, 0.5, 1.0

    def test_primitive_cell_for_cubic_lattice(self):
        pc = PrimitiveCell.for_cubic_lattice(self.a)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice, BravaisLattice.CUBIC)
        assert_array_equal(pc.p1, (self.a, 0, 0))
        assert_array_equal(pc.p2, (0, self.a, 0))
        assert_array_equal(pc.p3, (0, 0, self.a))

    def test_primitive_cell_for_body_centered_cubic_lattice(self):
        pc = PrimitiveCell.for_body_centered_cubic_lattice(self.a)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice,
                         BravaisLattice.BODY_CENTERED_CUBIC)
        assert_array_equal(pc.p1, (self.a, 0, 0))
        assert_array_equal(pc.p2, (0, self.a, 0))
        assert_array_equal(pc.p3, (self.a/2, self.a/2, self.a/2))

    def test_primitive_cell_for_face_centered_cubic_lattice(self):
        pc = PrimitiveCell.for_face_centered_cubic_lattice(self.a)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice,
                         BravaisLattice.FACE_CENTERED_CUBIC)
        assert_array_equal(pc.p1, (0, self.a/2, self.a/2))
        assert_array_equal(pc.p2, (self.a/2, 0, self.a/2))
        assert_array_equal(pc.p3, (self.a/2, self.a/2, 0))

    def test_primitive_cell_for_rhombohedral_lattice(self):
        cosa = np.cos(self.alpha)
        sina = np.sin(self.alpha)

        p1 = (self.a, 0, 0)
        p2 = (self.a*cosa, self.a*sina, 0)
        p3 = (self.a*cosa, self.a*(cosa-cosa**2) / sina,
              self.a*np.sqrt(sina**2 - ((cosa-cosa**2) / sina)**2))

        pc = PrimitiveCell.for_rhombohedral_lattice(self.a, self.alpha)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice,
                         BravaisLattice.RHOMBOHEDRAL)
        assert_array_equal(pc.p1, p1)
        assert_array_equal(pc.p2, p2)
        assert_array_equal(pc.p3, p3)

    def test_primitive_cell_for_tetragonal_lattice(self):
        pc = PrimitiveCell.for_tetragonal_lattice(self.a, self.c)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice,
                         BravaisLattice.TETRAGONAL)
        assert_array_equal(pc.p1, (self.a, 0, 0))
        assert_array_equal(pc.p2, (0, self.a, 0))
        assert_array_equal(pc.p3, (0, 0, self.c))

    def test_primitive_cell_for_body_centered_tetragonal_lattice(self):
        pc = PrimitiveCell.for_body_centered_tetragonal_lattice(self.a,
                                                                self.c)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice,
                         BravaisLattice.BODY_CENTERED_TETRAGONAL)
        assert_array_equal(pc.p1, (self.a, 0, 0))
        assert_array_equal(pc.p2, (0, self.a, 0))
        assert_array_equal(pc.p3, (self.a/2, self.a/2, self.c/2))

    def test_primitive_cell_for_hexagonal_lattice(self):
        pc = PrimitiveCell.for_hexagonal_lattice(self.a, self.c)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice,
                         BravaisLattice.HEXAGONAL)
        assert_array_equal(pc.p1, (self.a, 0, 0))
        assert_array_equal(pc.p2, (self.a/2, self.a*np.sqrt(3)/2, 0))
        assert_array_equal(pc.p3, (0, 0, self.c))

    def test_primitive_cell_for_orthorhombic_lattice(self):
        pc = PrimitiveCell.for_orthorhombic_lattice(self.a, self.b, self.c)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice,
                         BravaisLattice.ORTHORHOMBIC)
        assert_array_equal(pc.p1, (self.a, 0, 0))
        assert_array_equal(pc.p2, (0, self.b, 0))
        assert_array_equal(pc.p3, (0, 0, self.c))

    def test_primitive_cell_for_body_centered_orthorhombic_lattice(self):
        pc = PrimitiveCell.for_body_centered_orthorhombic_lattice(
            self.a, self.b, self.c)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice,
                         BravaisLattice.BODY_CENTERED_ORTHORHOMBIC)
        assert_array_equal(pc.p1, (self.a, 0, 0))
        assert_array_equal(pc.p2, (0, self.b, 0))
        assert_array_equal(pc.p3, (self.a/2, self.b/2, self.c/2))

    def test_primitive_cell_for_face_centered_orthorhombic_lattice(self):
        pc = PrimitiveCell.for_face_centered_orthorhombic_lattice(
            self.a, self.b, self.c)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice,
                         BravaisLattice.FACE_CENTERED_ORTHORHOMBIC)
        assert_array_equal(pc.p1, (0, self.b/2, self.c/2))
        assert_array_equal(pc.p2, (self.a/2, 0, self.c/2))
        assert_array_equal(pc.p3, (self.a/2, self.b/2, 0))

    def test_primitive_cell_for_base_centered_orthorhombic_lattice(self):
        pc = PrimitiveCell.for_base_centered_orthorhombic_lattice(
            self.a, self.b, self.c)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice,
                         BravaisLattice.BASE_CENTERED_ORTHORHOMBIC)
        assert_array_equal(pc.p1, (self.a, 0, 0))
        assert_array_equal(pc.p2, (self.a/2, self.b/2, 0))
        assert_array_equal(pc.p3, (0, 0, self.c))

    def test_primitive_cell_for_monoclinic_lattice(self):
        pc = PrimitiveCell.for_monoclinic_lattice(
            self.a, self.b, self.c, self.beta)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice,
                         BravaisLattice.MONOCLINIC)
        assert_array_equal(pc.p1,
                           (self.a*np.sin(self.beta), 0,
                            self.a*np.cos(self.beta)))
        assert_array_equal(pc.p2, (0, self.b, 0))
        assert_array_equal(pc.p3, (0, 0, self.c))

    def test_primitive_cell_for_base_centered_monoclinic_lattice(self):
        p1 = (self.a*np.sin(self.beta), 0, self.a*np.cos(self.beta))
        p2 = (self.a*np.sin(self.beta)/2, self.b/2,
              self.a*np.cos(self.beta)/2)

        pc = PrimitiveCell.for_base_centered_monoclinic_lattice(
            self.a, self.b, self.c, self.beta)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice,
                         BravaisLattice.BASE_CENTERED_MONOCLINIC)
        assert_array_equal(pc.p1, p1)
        assert_array_equal(pc.p2, p2)
        assert_array_equal(pc.p3, (0, 0, self.c))

    def test_primitive_cell_for_triclinic_lattice(self):
        cosa = np.cos(self.alpha)
        cosb = np.cos(self.beta)
        sinb = np.sin(self.beta)
        cosg = np.cos(self.gamma)
        sing = np.sin(self.gamma)

        p1 = (self.a, 0, 0)
        p2 = (self.b*cosg, self.b*sing, 0)
        p3 = (self.c*cosb, self.c*(cosa-cosb*cosg) / sing,
              self.c*np.sqrt(sinb**2 - ((cosa-cosb*cosg) / sing)**2))

        pc = PrimitiveCell.for_triclinic_lattice(
            self.a, self.b, self.c, self.alpha, self.beta, self.gamma)
        self.assertIsInstance(pc, PrimitiveCell)
        self.assertEqual(pc.bravais_lattice,
                         BravaisLattice.TRICLINIC)
        assert_array_equal(pc.p1, p1)
        assert_array_equal(pc.p2, p2)
        assert_array_equal(pc.p3, p3)
