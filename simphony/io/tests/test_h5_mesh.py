import os
import tempfile
import shutil
import unittest
import tables

from simphony.core.cuba import CUBA
from simphony.testing.abc_check_mesh import (
    CheckMeshPointOperations, CheckMeshEdgeOperations,
    CheckMeshFaceOperations, CheckMeshCellOperations,
    CheckMeshContainer)
from simphony.io.h5_mesh import H5Mesh


class TestH5MeshPointOperations(CheckMeshPointOperations, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')
        CheckMeshPointOperations.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name):
        group = self.handle.create_group(self.handle.root, name)
        return H5Mesh(group, self.handle)

    def supported_cuba(self):
        return set(CUBA)


class TestH5MeshEdgeOperations(CheckMeshEdgeOperations, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')
        CheckMeshEdgeOperations.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name):
        group = self.handle.create_group(self.handle.root, name)
        return H5Mesh(group, self.handle)

    def supported_cuba(self):
        return set(CUBA)


class TestH5MeshFaceOperations(CheckMeshFaceOperations, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')
        CheckMeshFaceOperations.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name):
        group = self.handle.create_group(self.handle.root, name)
        return H5Mesh(group, self.handle)

    def supported_cuba(self):
        return set(CUBA)


class TestH5MeshCellOperations(CheckMeshCellOperations, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')
        CheckMeshCellOperations.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name):
        group = self.handle.create_group(self.handle.root, name)
        return H5Mesh(group, self.handle)

    def supported_cuba(self):
        return set(CUBA)


class TestH5Mesh(CheckMeshContainer, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')
        CheckMeshContainer.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name):
        group = self.handle.create_group(self.handle.root, name)
        return H5Mesh(group, self.handle)

    def supported_cuba(self):
        return set(CUBA)


class TestH5MeshStoredLayout(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def test_new_mesh_layout(self):
        # given
        group = self.handle.create_group(self.handle.root, 'test')

        # when
        H5Mesh(group, self.handle)

        # when
        self.assertEqual(len(group._f_list_nodes()), 6)
        self.assertIsInstance(group.cells, tables.Table)
        self.assertIsInstance(group.points, tables.Table)
        self.assertIsInstance(group.edges, tables.Table)
        self.assertIsInstance(group.faces, tables.Table)
        self.assertIsInstance(group.data, tables.Table)
        self.assertIsInstance(group.item_data, tables.Table)

    def test_mesh_layout_with_new_proxy(self):
        # when
        group = self.handle.create_group(self.handle.root, 'test')

        # when creating a proxy mesh twice
        H5Mesh(group, self.handle)  # this will create the layout
        H5Mesh(group, self.handle)

        # then
        self.assertEqual(len(group._f_list_nodes()), 6)
        self.assertIsInstance(group.cells, tables.Table)
        self.assertIsInstance(group.points, tables.Table)
        self.assertIsInstance(group.edges, tables.Table)
        self.assertIsInstance(group.faces, tables.Table)
        self.assertIsInstance(group.data, tables.Table)
        self.assertIsInstance(group.item_data, tables.Table)


class TestH5MeshVersions(unittest.TestCase):

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
            H5Mesh(group, handle)

            # then
            self.assertTrue(isinstance(group._v_attrs.cuds_version, int))

        # when
        with tables.open_file(filename, 'a') as handle:
            handle.get_node("/" + group_name)._v_attrs.cuds_version = -1

        # then
        with tables.open_file(filename, 'a') as handle:
            with self.assertRaises(ValueError):
                H5Mesh(handle.get_node("/" + group_name), handle)


if __name__ == '__main__':
    unittest.main()
