import os
import tempfile
import shutil
import unittest
import tables

from simphony.cuds.mesh import Mesh
from simphony.testing.abc_check_mesh import (
    MeshPointOperationsCheck, MeshEdgeOperationsCheck,
    MeshFaceOperationsCheck, MeshCellOperationsCheck)

from simphony.io.h5_mesh import H5Mesh


class TestH5MeshPointOperations(MeshPointOperationsCheck, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')
        MeshPointOperationsCheck.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name):
        group = self.handle.create_group(self.handle.root, name)
        return H5Mesh(group, self.handle)


class TestH5MeshEdgeOperations(MeshEdgeOperationsCheck, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')
        MeshEdgeOperationsCheck.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name):
        group = self.handle.create_group(self.handle.root, name)
        return H5Mesh(group, self.handle)


class TestH5MeshFaceOperations(MeshFaceOperationsCheck, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')
        MeshFaceOperationsCheck.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name):
        group = self.handle.create_group(self.handle.root, name)
        return H5Mesh(group, self.handle)


class TestH5MeshCellOperations(MeshCellOperationsCheck, unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = tables.open_file(self.filename, mode='w')
        MeshCellOperationsCheck.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)

    def container_factory(self, name):
        group = self.handle.create_group(self.handle.root, name)
        return H5Mesh(group, self.handle)


if __name__ == '__main__':
    unittest.main()
