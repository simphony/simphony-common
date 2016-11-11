import os
import tempfile
import shutil
import unittest
import tables

from simphony.io.h5_lattice import H5Lattice
from simphony.io.data_container_description import SUPPORTED_CUBA
from simphony.cuds.primitive_cell import (PrimitiveCell, BravaisLattice)
from numpy.testing import (assert_array_equal, assert_array_almost_equal)
from simphony.core import CUBA
from simphony.testing.abc_check_lattice import (
    CheckLatticeContainer, CheckLatticeNodeOperations,
    CheckLatticeNodeCoordinates)


class CustomRecord(tables.IsDescription):
    class data(tables.IsDescription):

        velocity = tables.Float64Col(pos=1, shape=3)
        density = tables.Float64Col(pos=2)

    mask = tables.BoolCol(pos=1, shape=(3,))


class TestH5LatticeProperties(CheckLatticeContainer, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')
        CheckLatticeContainer.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name, primitive_cell, size, origin):
        self.group = self.handle.create_group(
            self.handle.root, name)
        return H5Lattice.create_new(self.group, primitive_cell, size, origin)

    def supported_cuba(self):
        return SUPPORTED_CUBA

    def test_initialization_from_existing_lattice_in_file(self):
        lattice = H5Lattice(self.group)
        self.assertEqual(lattice.name, 'my_name')
        self.assertEqual(lattice.primitive_cell.bravais_lattice,
                         BravaisLattice.CUBIC)
        assert_array_almost_equal(lattice.primitive_cell.p1,
                                  self.primitive_cell.p1)
        assert_array_almost_equal(lattice.primitive_cell.p2,
                                  self.primitive_cell.p2)
        assert_array_almost_equal(lattice.primitive_cell.p3,
                                  self.primitive_cell.p3)
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

    def container_factory(self, name, primitive_cell, size, origin):
        self.group = self.handle.create_group(
            self.handle.root, name)
        return H5Lattice.create_new(self.group, primitive_cell, size, origin)

    def supported_cuba(self):
        return SUPPORTED_CUBA


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

    def container_factory(self, name, primitive_cell, size, origin):
        self.group = self.handle.create_group(
            self.handle.root, name)
        return H5Lattice.create_new(self.group, primitive_cell, size, origin)

    def supported_cuba(self):
        return SUPPORTED_CUBA


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

    def container_factory(self, name, primitive_cell, size, origin):
        self.group = self.handle.create_group(
            self.handle.root, name)
        return H5Lattice.create_new(self.group, primitive_cell, size,
                                    origin, record=CustomRecord)

    def supported_cuba(self):
        return [CUBA.VELOCITY, CUBA.DENSITY]


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

    def container_factory(self, name, primitive_cell, size, origin):
        self.group = self.handle.create_group(self.handle.root, name)
        return H5Lattice.create_new(self.group, primitive_cell, size,
                                    origin, record=CustomRecord)

    def supported_cuba(self):
        return [CUBA.VELOCITY, CUBA.DENSITY]


class TestH5LatticeVersions(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_version(self):
        filename = os.path.join(self.temp_dir, 'test_file.cuds')
        group_name = "dummy_component_name"
        with tables.open_file(filename, 'w') as handle:
            group = handle.create_group(handle.root, group_name)

            # given/when
            H5Lattice.create_new(group, PrimitiveCell.for_cubic_lattice(0.2),
                                 size=(5, 10, 15), origin=(-2, 0, 1))

            # then
            self.assertTrue(isinstance(group._v_attrs.cuds_version, int))

        # when
        with tables.open_file(filename, 'a') as handle:
            handle.get_node(
                "/{}".format(group_name))._v_attrs.cuds_version = -1

        # then
        with tables.open_file(filename, 'a') as handle:
            with self.assertRaises(ValueError):
                H5Lattice(handle.get_node("/" + group_name))

if __name__ == '__main__':
    unittest.main()
