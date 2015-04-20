import unittest

from simphony.cuds.mesh import Mesh
from simphony.testing.abc_check_mesh import (
    MeshPointOperationsCheck, MeshEdgeOperationsCheck,
    MeshFaceOperationsCheck, MeshCellOperationsCheck,
    MeshAttributesCheck)


class TestMeshPointOperations(MeshPointOperationsCheck, unittest.TestCase):

    def container_factory(self, name):
        return Mesh(name=name)


class TestMeshEdgeOperations(MeshEdgeOperationsCheck, unittest.TestCase):

    def container_factory(self, name):
        return Mesh(name=name)


class TestMeshFaceOperations(MeshFaceOperationsCheck, unittest.TestCase):

    def container_factory(self, name):
        return Mesh(name=name)


class TestMeshCellOperations(MeshCellOperationsCheck, unittest.TestCase):

    def container_factory(self, name):
        return Mesh(name=name)


class TestMeshAttributes(MeshAttributesCheck, unittest.TestCase):

    def container_factory(self, name):
        return Mesh(name=name)


if __name__ == '__main__':
    unittest.main()
