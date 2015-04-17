""" test_mesh module

This module contains the unitary tests for the
mesh module functionalities

"""

import unittest

from functools import partial

from simphony.testing.utils import compare_data_containers

from simphony.cuds.mesh import Mesh
from simphony.cuds.mesh import Point
from simphony.cuds.mesh import Edge
from simphony.cuds.mesh import Face
from simphony.cuds.mesh import Cell

from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer

from simphony.testing.abc_check_mesh import (
    MeshPointOperationsCheck, MeshEdgeOperationsCheck,
    MeshFaceOperationsCheck, MeshCellOperationsCheck)


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



if __name__ == '__main__':
    unittest.main()
