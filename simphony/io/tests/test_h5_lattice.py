import os
import tempfile
import shutil
import unittest
import tables

from simphony.io.h5_lattice import H5Lattice
from numpy.testing import assert_array_equal
from simphony.core.cuba import CUBA
from simphony.testing.abc_check_lattice import ABCCheckLattice
from simphony.core.data_container import DataContainer


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
        self.group = self.handle.create_group(
            self.handle.root, name)
        return H5Lattice.create_new(
            self.group, type_, base_vect, size, origin)

    def supported_cuba(self):
        return set(CUBA)

    def test_initialization_from_existing_lattice_in_file(self):
        """ Checks that H5Lattice constructed from Lattice with a
        CustomRecord column description has correct attributes
        """
        lattice = H5Lattice(self.group)
        self.assertEqual(lattice.name, 'foo')
        self.assertEqual(lattice.type, 'Cubic')
        assert_array_equal(lattice.base_vect, self.base_vect)
        self.assertItemsEqual(lattice.size, self.size)
        assert_array_equal(lattice.origin, self.origin)

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
        self.group = self.handle.create_group(
            self.handle.root, name)
        return H5Lattice.create_new(self.group, type_, base_vect, size,
                                    origin, record=CustomRecord)

    def supported_cuba(self):
        return [CUBA.VELOCITY, CUBA.MATERIAL_ID, CUBA.DENSITY]

    def test_initialization_from_existing_lattice_in_file(self):
        """ Checks that H5Lattice constructed from Lattice with a
        CustomRecord column description has correct attributes
        """
        lattice = H5Lattice(self.group)
        self.assertEqual(lattice.name, 'foo')
        self.assertEqual(lattice.type, 'Cubic')
        assert_array_equal(lattice.base_vect, self.base_vect)
        self.assertItemsEqual(lattice.size, self.size)
        assert_array_equal(lattice.origin, self.origin)


if __name__ == '__main__':
    unittest.main()
