import os
import tempfile
import shutil
import unittest
import tables
import numpy

from simphony.cuds.lattice import Lattice
from simphony.cuds.lattice import LatticeNode
from simphony.cuds.lattice import make_hexagonal_lattice
from simphony.cuds.lattice import make_orthorombicp_lattice
from simphony.io.file_lattice import FileLattice
from numpy.testing import assert_array_equal
from numpy.testing import assert_equal
from simphony.testing.utils import compare_data_containers
from simphony.core.cuba import CUBA
from simphony.io.h5_cuds import H5CUDS
from simphony.testing.abc_check_lattice import ABCCheckLattice


class CustomRecord(tables.IsDescription):

    class data(tables.IsDescription):

        material_id = tables.Int32Col(pos=0)
        velocity = tables.Float64Col(pos=1, shape=3)
        density = tables.Float64Col(pos=2)

    mask = tables.BoolCol(pos=1, shape=(3,))


class TestFileLattice(ABCCheckLattice, unittest.TestCase):
    """ Basic testing of the FileLattice.
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = H5CUDS.open(self.filename)
        ABCCheckLattice.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name, type_, base_vect, size, origin):
        lattice = Lattice(name, type_, base_vect, size, origin)
        self.handle.add_lattice(lattice)
        return self.handle.get_lattice(name)

    def supported_cuba(self):
        return set(CUBA)

    def test_initialization_from_existing_lattice_in_file(self):
        """ Checks that FileLattice constructed from a known table already
        existing in H5CUDS-file provides correct attributes for FileLattice
        object

        """
        lattice = FileLattice(self.handle._handle, 'foo')
        self.assertEqual(lattice.name, 'foo')
        self.assertEqual(lattice.type, 'Cubic')
        assert_array_equal(lattice.base_vect, self.base_vect)
        self.assertItemsEqual(lattice.size, self.size)
        assert_array_equal(lattice.origin, self.origin)


class TestFileLatticeCustom(ABCCheckLattice, unittest.TestCase):
    """ TestFileLattice using a custom record.

    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = H5CUDS.open(self.filename)
        ABCCheckLattice.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name, type_, base_vect, size, origin):
        print base_vect
        return FileLattice(
            self.handle._handle, 'foo', type_, base_vect,
            size, origin, record=CustomRecord)

    def supported_cuba(self):
        return [CUBA.VELOCITY, CUBA.MATERIAL_ID, CUBA.DENSITY]


if __name__ == '__main__':
    unittest.main()
