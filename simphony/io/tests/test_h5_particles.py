import os
import tempfile
import shutil
import unittest

import tables

from simphony.cuds.particles import Particles
from simphony.io.h5_cuds import H5CUDS
from simphony.io.h5_particles import H5Particles
from simphony.core.cuba import CUBA
from simphony.testing.abc_check_particles import (
    ContainerManipulatingBondsCheck, ContainerAddParticlesCheck,
    ContainerAddBondsCheck, ContainerManipulatingParticlesCheck)


class TestH5ContainerAddParticles(
        ContainerAddParticlesCheck, unittest.TestCase):

    def container_factory(self, name):
        self.handle.add_dataset(Particles(name=name))
        return self.handle.get_dataset(name)

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
        self.handle.add_dataset(Particles(name=name))
        return self.handle.get_dataset(name)

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
        self.handle.add_dataset(Particles(name=name))
        return self.handle.get_dataset(name)

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
        self.handle.add_dataset(Particles(name=name))
        return self.handle.get_dataset(name)

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


class TestH5ParticlesVersions(unittest.TestCase):

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
            H5Particles(group)

            # then
            self.assertTrue(isinstance(group._v_attrs.cuds_version, int))

        # when
        with tables.open_file(filename, 'a') as handle:
            handle.get_node("/" + group_name)._v_attrs.cuds_version = -1

        # then
        with tables.open_file(filename, 'a') as handle:
            with self.assertRaises(ValueError):
                H5Particles(handle.get_node("/" + group_name))


if __name__ == '__main__':
    unittest.main()
