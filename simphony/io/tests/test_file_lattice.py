import os
import tempfile
import shutil
import unittest
import tables
import numpy

from simphony.cuds.lattice import Lattice
from simphony.cuds.lattice import LatticeNode
from simphony.io.file_lattice import FileLattice
from numpy.testing import assert_array_equal
from numpy.testing import assert_equal
from simphony.testing.utils import compare_data_containers

from simphony.core.cuba import CUBA

from simphony.io.h5_cuds import H5CUDS


class CustomRecord(tables.IsDescription):

    class data(tables.IsDescription):

        material_id = tables.Int32Col(pos=0)
        velocity = tables.Float64Col(pos=1, shape=3)
        density = tables.Float64Col(pos=2)

    mask = tables.BoolCol(pos=1, shape=(3,))


class TestFileLattice(unittest.TestCase):

    def setUp(self):

        self.temp_dir = tempfile.mkdtemp()

        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.file = H5CUDS.open(self.filename, mode='w')

        self.lattice = Lattice('test_lattice', 'cubic', (1.0, 1.0, 1.0),
                               (4, 5, 6), (0.0, 0.0, 0.0))

        for i in xrange(4):
            for j in xrange(5):
                for k in xrange(6):
                    N = LatticeNode((i, j, k), {CUBA.MATERIAL_ID: 1})
                    self.lattice.update_node(N)

        for i in xrange(2):
            for j in xrange(3):
                for k in xrange(6):
                    N = LatticeNode((i+1, j+1, k),
                                    {CUBA.MATERIAL_ID: 0,
                                     CUBA.DENSITY: 1.0,
                                     CUBA.VELOCITY: [0.0, 0.0, 1.0]})
                    self.lattice.update_node(N)

        lat = self.lattice
        self.filelattice = FileLattice(self.file._handle, lat.name, lat.type,
                                       lat.base_vect, lat.size, lat.origin,
                                       CustomRecord)
        for N in lat.iter_nodes():
            self.filelattice.update_node(N)

    def tearDown(self):
        if os.path.exists(self.filename):
            self.file.close()
        shutil.rmtree(self.temp_dir)

    def test_file_lattice_constructed_from_Lattice(self):
        """ Checks that FileLattice constructed from Lattice with a
        CustomRecord column description has correct attributes

        """
        self.assertEqual(self.filelattice.name, 'test_lattice')
        self.assertEqual(self.filelattice.type, 'cubic')
        assert_array_equal(self.filelattice.base_vect,
                           numpy.array((1.0, 1.0, 1.0)))
        self.assertItemsEqual(self.filelattice.size, (4, 5, 6))
        assert_array_equal(self.filelattice.origin,
                           numpy.array((0.0, 0.0, 0.0)))

    def test_file_lattice_constructed_from_table_existing_in_file(self):
        """ Checks that FileLattice constructed from a known table already
        existing in H5CUDS-file provides correct attributes for FileLattice
        object

        """
        self.filelattice = self.file.get_lattice('test_lattice')

        self.assertEqual(self.filelattice.name, 'test_lattice')
        self.assertEqual(self.filelattice.type, 'cubic')
        assert_array_equal(self.filelattice.base_vect,
                           numpy.array((1.0, 1.0, 1.0)))
        self.assertItemsEqual(self.filelattice.size, (4, 5, 6))
        assert_array_equal(self.filelattice.origin,
                           numpy.array((0.0, 0.0, 0.0)))

    def test_get_node(self):
        """ Check that a LatticeNode can be retrieved correctly

        """
        N = self.filelattice.get_node((3, 3, 3))

        self.assertTrue(isinstance(N, LatticeNode))
        self.assertItemsEqual(N.index, (3, 3, 3))

        for key, value in self.lattice.get_node((3, 3, 3)).data.iteritems():
            assert_equal(N.data[key], value)

    def test_node_iterator(self):
        """ Checks the node iterator

        Checks that an iterator over all
        the nodes is returned when the function iter_nodes is called
        without arguments

        """
        fl_nodes = self.filelattice.iter_nodes()

        for M in fl_nodes:
            N = self.lattice.get_node(M.index)
            self.assertEqual(N.index, M.index)
            compare_data_containers(N.data, M.data, testcase=self)

    def test_node_iterator_subset(self):
        """ Checks the node iterator on a subset of nodes

        """
        fl_nodes = self.filelattice.iter_nodes([(0, 0, 0), (0, 1, 2)])

        for M in fl_nodes:
            N = self.lattice.get_node(M.index)
            self.assertEqual(N.index, M.index)
            compare_data_containers(N.data, M.data, testcase=self)

    def test_update_node(self):
        """ Check that a node can be updated correctly

        """
        N = LatticeNode((3, 2, 3),
                        {CUBA.MATERIAL_ID: 2, CUBA.DENSITY: 10.0,
                         CUBA.VELOCITY: (0.0, 0.0, 10.0)})

        self.filelattice.update_node(N)

        M = self.filelattice.get_node((3, 2, 3))

        self.assertEqual(N.index, M.index)
        compare_data_containers(N.data, M.data, testcase=self)

    def test_update_node_with_extra_keywords(self):
        """ Check that a node can be updated correctly when a LatticeNode has
        some CUBA-keys defined that do not exist in the FileLattice.

        """
        N = LatticeNode((2, 3, 4),
                        {CUBA.MATERIAL_ID: 2, CUBA.DENSITY: 10.0,
                         CUBA.VELOCITY: (0.0, 0.0, 100.0),
                         CUBA.DISTRIBUTION: (1.0, 1.1, 1.2, 1.3, 1.4)})

        self.filelattice.update_node(N)

        M = self.filelattice.get_node((2, 3, 4))

        self.assertEqual(N.index, M.index)
        for key in M.data:
            self.assertIn(key, M.data)
            assert_equal(N.data[key], M.data[key])

if __name__ == '__main__':
    unittest.main()
