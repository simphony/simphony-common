import os
import tempfile
import shutil
import unittest
import tables

from simphony.io.h5_lattice import H5Lattice
from numpy.testing import assert_array_equal
from simphony.core.cuba import CUBA
from simphony.testing.abc_check_lattice import (
    CheckLatticeProperties, CheckLatticeNodeOperations,
    CheckLatticeNodeCoordinates)


class CustomRecord(tables.IsDescription):

    class data(tables.IsDescription):

        material_id = tables.Int32Col(pos=0)
        velocity = tables.Float64Col(pos=1, shape=3)
        density = tables.Float64Col(pos=2)

    mask = tables.BoolCol(pos=1, shape=(3,))


class TestH5LatticeProperties(CheckLatticeProperties, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')
        CheckLatticeProperties.setUp(self)

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
        lattice = H5Lattice(self.group)
        self.assertEqual(lattice.name, 'my_name')
        self.assertEqual(lattice.type, 'Cubic')
        assert_array_equal(lattice.base_vect, self.base_vect)
        self.assertItemsEqual(lattice.size, self.size)
        assert_array_equal(lattice.origin, self.origin)


class TestH5LatticeNodeCoordinates(
        CheckLatticeNodeCoordinates, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')

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

    @unittest.skip('Hexagonal coordinates are not supported yet')
    def test_get_coordinate_hexagonal(self):
        pass

class TestH5LatticeNodeOperations(
        CheckLatticeNodeOperations, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')
        CheckLatticeNodeOperations.setUp(self)

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


class TestH5LatticeNodeCustomCoordinates(
        CheckLatticeNodeCoordinates, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, 'w')

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

    @unittest.skip('Hexagonal coordinates are not supported yet')
    def test_get_coordinate_hexagonal(self):
        pass


class TestH5LatticeCustomNodeOperations(
        CheckLatticeNodeOperations, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, 'w')
        CheckLatticeNodeOperations.setUp(self)

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


if __name__ == '__main__':
    unittest.main()
