import copy
import os
import tempfile
import shutil
import unittest

import unittest
from simphony.cuds.mesh import Mesh
from simphony.cuds.mesh import Point
from simphony.cuds.mesh import Edge
from simphony.cuds.mesh import Face
from simphony.cuds.mesh import Cell

from simphony.io.cuds_file import CudsFile


class TestFileMeshContainer(unittest.TestCase):

    def setUp(self):

        self.temp_dir = tempfile.mkdtemp()
        
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.file = CudsFile.open(self.filename)

        self.pids = []
        self.mesh = Mesh()

        self.points = [
            Point(
                None,
                (0.0, 0.0, 0.0),
                dc.DataContainer(),
                dc.DataContainer()
                ),
            Point(
                None,
                (1.0, 0.0, 0.0),
                dc.DataContainer(),
                dc.DataContainer()
                ),
            Point(
                None,
                (0.0, 1.0, 0.0),
                dc.DataContainer(),
                dc.DataContainer()
                ),
            Point(
                None,
                (0.0, 0.0, 1.0),
                dc.DataContainer(),
                dc.DataContainer()
                ),
            Point(
                None,
                (1.0, 0.0, 1.0),
                dc.DataContainer(),
                dc.DataContainer()
                ),
            Point(
                None,
                (0.0, 1.0, 1.0),
                dc.DataContainer(),
                dc.DataContainer()
                )
        	]

        for point in self.points:
            pid = self.mesh.add_point(point)
            pids.append(pid)

        self.edges = [
            Edge(None, pids[0:2], dc.DataContainer(), dc.DataContainer()),
            Edge(None, pids[1:3], dc.DataContainer(), dc.DataContainer())
        ]

        self.faces = [
            Face(None, pids[0:3], dc.DataContainer(), dc.DataContainer()),
            Face(None, pids[1:4], dc.DataContainer(), dc.DataContainer())
        ]

        self.cells = [
            Cell(None, pids[0:4], dc.DataContainer(), dc.DataContainer()),
            Cell(None, pids[1:5], dc.DataContainer(), dc.DataContainer())
            ]

    def tearDown(self):
        if os.path.exists(self.filename):
            self.file.close()
        shutil.rmtree(self.temp_dir)