import os
import tempfile
import shutil
import unittest
import tables

from simphony.io.h5_lattice import H5Lattice
from numpy.testing import assert_array_equal
from simphony.core.cuba import CUBA
from simphony.testing.abc_check_lattice import ABCCheckLattice


class CustomRecord(tables.IsDescription):

    class data(tables.IsDescription):

        material_id = tables.Int32Col(pos=0)
        velocity = tables.Float64Col(pos=1, shape=3)
        density = tables.Float64Col(pos=2)

    mask = tables.BoolCol(pos=1, shape=(3,))


class TestH5Lattice(ABCCheckLattice, unittest.TestCase):
    """ Basic testing of the H5Lattice.
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')
        ABCCheckLattice.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name, type_, base_vect, size, origin):
        return H5Lattice.create_new(
            self.handle.root, name, type_, base_vect, size, origin)

    def supported_cuba(self):
        return set(CUBA)

    def test_initialization_from_existing_lattice_in_file(self):
        """ Checks that H5Lattice constructed from Lattice with a
        CustomRecord column description has correct attributes
        """
        lattice = H5Lattice(self.handle.root, 'foo')
        self.assertEqual(lattice.name, 'foo')
        self.assertEqual(lattice.type, 'Cubic')
        assert_array_equal(lattice.base_vect, self.base_vect)
        self.assertItemsEqual(lattice.size, self.size)
        assert_array_equal(lattice.origin, self.origin)


class TestFileLatticeCustom(ABCCheckLattice, unittest.TestCase):
    """ Test H5Lattice using a custom record.
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, 'w')
        ABCCheckLattice.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name, type_, base_vect, size, origin):
        return H5Lattice.create_new(
            self.handle.root, 'foo', type_, base_vect,
            size, origin, record=CustomRecord)

    def supported_cuba(self):
        return [CUBA.VELOCITY, CUBA.MATERIAL_ID, CUBA.DENSITY]


if __name__ == '__main__':
    unittest.main()
