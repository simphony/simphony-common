import os
import tempfile
import shutil
import unittest

from simphony.cuds.particles import Particles
from simphony.io.h5_cuds import H5CUDS
from simphony.core.cuba import CUBA
from simphony.testing.abc_check_particles import (
    ContainerManipulatingBondsCheck, ContainerAddParticlesCheck,
    ContainerAddBondsCheck, ContainerManipulatingParticlesCheck)


class TestH5ContainerAddParticles(
        ContainerAddParticlesCheck, unittest.TestCase):

    def container_factory(self, name):
        return self.handle.add_particles(
            Particles(name=name))

    def supported_cuba(self):
        return set(CUBA)

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = H5CUDS.open(self.filename)
        ContainerAddParticlesCheck.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)


class TestH5ContainerManipulatingParticles(
        ContainerManipulatingParticlesCheck, unittest.TestCase):

    def container_factory(self, name):
        return self.handle.add_particles(
            Particles(name=name))

    def supported_cuba(self):
        return set(CUBA)

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = H5CUDS.open(self.filename)
        ContainerManipulatingParticlesCheck.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)


class TestH5ContainerAddBonds(ContainerAddBondsCheck, unittest.TestCase):

    def container_factory(self, name):
        return self.handle.add_particles(
            Particles(name=name))

    def supported_cuba(self):
        return set(CUBA)

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = H5CUDS.open(self.filename)
        ContainerAddBondsCheck.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)


class TestH5ContainerManipulatingBonds(
        ContainerManipulatingBondsCheck, unittest.TestCase):

    def container_factory(self, name):
        return self.handle.add_particles(
            Particles(name=name))

    def supported_cuba(self):
        return set(CUBA)

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.addCleanup(self.cleanup)
        self.handle = H5CUDS.open(self.filename)
        ContainerManipulatingBondsCheck.setUp(self)

    def cleanup(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    unittest.main()
