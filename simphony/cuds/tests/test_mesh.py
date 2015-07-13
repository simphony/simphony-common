import unittest

from simphony.core.cuba import CUBA
from simphony.cuds.mesh import Mesh
from simphony.testing.abc_check_mesh import (
    CheckMeshPointOperations, CheckMeshEdgeOperations,
    CheckMeshFaceOperations, CheckMeshCellOperations,
    CheckMeshContainer)


class TestMeshPointOperations(CheckMeshPointOperations, unittest.TestCase):

    def container_factory(self, name):
        return Mesh(name=name)

    def supported_cuba(self):
        return set(CUBA)


class TestMeshEdgeOperations(CheckMeshEdgeOperations, unittest.TestCase):

    def container_factory(self, name):
        return Mesh(name=name)

    def supported_cuba(self):
        return set(CUBA)


class TestMeshFaceOperations(CheckMeshFaceOperations, unittest.TestCase):

    def container_factory(self, name):
        return Mesh(name=name)

    def supported_cuba(self):
        return set(CUBA)


class TestMeshCellOperations(CheckMeshCellOperations, unittest.TestCase):

    def container_factory(self, name):
        return Mesh(name=name)

    def supported_cuba(self):
        return set(CUBA)


class TestMeshContainer(CheckMeshContainer, unittest.TestCase):

    def container_factory(self, name):
        return Mesh(name=name)

    def supported_cuba(self):
        return set(CUBA)


if __name__ == '__main__':
    unittest.main()
