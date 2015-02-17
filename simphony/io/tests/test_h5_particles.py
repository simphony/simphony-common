import copy
import os
import tempfile
import shutil
import unittest
import uuid

from simphony.cuds.particles import ParticleContainer, Particle, Bond
from simphony.io.h5_cuds import H5CUDS
from simphony.cuds.tests.abc_check_particle_containers import (
    ContainerManipulatingBondsCheck, ContainerAddParticlesCheck,
    ContainerAddBondsCheck, ContainerManipulatingParticlesCheck)


class TestH5ContainerAddParticles(
        ContainerAddParticlesCheck, unittest.TestCase):

    def container_factory(self, name):
        return self.handle.add_particle_container(
            ParticleContainer(name=name))

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
        return self.handle.add_particle_container(
            ParticleContainer(name=name))

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.handle = H5CUDS.open(self.filename)
        ContainerManipulatingParticlesCheck.setUp(self)

    def tearDown(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)


class TestH5ContainerAddBonds(ContainerAddBondsCheck, unittest.TestCase):

    def container_factory(self, name):
        return self.handle.add_particle_container(
            ParticleContainer(name=name))

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.handle = H5CUDS.open(self.filename)
        ContainerAddBondsCheck.setUp(self)

    def tearDown(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)


class TestH5ContainerManipulatingBonds(
        ContainerManipulatingBondsCheck):

    def container_factory(self, name):
        return self.handle.add_particle_container(
            ParticleContainer(name=name))

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.handle = H5CUDS.open(self.filename)
        ContainerManipulatingBondsCheck.setUp(self)

    def tearDown(self):
        if os.path.exists(self.filename):
            self.handle.close()
        shutil.rmtree(self.temp_dir)


class _TestFileParticleContainer(object):

    def setUp(self):

        # create file with empty particle container
        self.pc = 23

        # create two particles (with unique ids)
        self.particle_1 = Particle(
            (0.1, 0.4, 5.0), uid=uuid.UUID(int=0, version=4))
        self.particle_2 = Particle(
            (0.2, 0.45, 50.0), uid=uuid.UUID(int=1, version=4))

        # create two bonds (with unique ids)
        self.bond_1 = Bond((1, 0), uid=uuid.UUID(int=2, version=4))
        self.bond_2 = Bond((0, 1), uid=uuid.UUID(int=3, version=4))

    def test_add_get_particle(self):
        self.pc.add_particle(self.particle_1)
        particles = self.pc.get_particle(self.particle_1.uid)
        self.assertTrue(particles is not self.particle_1)
        self.assertEqual(particles.uid, self.particle_1.uid)
        self.assertEqual(particles.coordinates, self.particle_1.coordinates)

    def test_add_particle_with_same_id(self):
        self.pc.add_particle(self.particle_1)
        with self.assertRaises(Exception):
            self.pc.add_particle(self.particle_1)

    def test_has_particle_ok(self):
        self.pc.add_particle(self.particle_1)
        self.assertTrue(self.pc.has_particle(self.particle_1.uid))

    def test_has_particle_false(self):
        self.assertFalse(self.pc.has_particle(self.particle_1))

    def test_add_get_particle_with_default_id(self):
        p = Particle((1.0, 1.0, 0.0))
        uid = self.pc.add_particle(p)
        particle = self.pc.get_particle(uid)
        self.assertTrue(particle is not p)
        self.assertEqual(particle.uid, uid)
        self.assertEqual(particle.coordinates, p.coordinates)

    def test_get_particle_throws(self):
        with self.assertRaises(Exception):
            self.pc.get_particle(0)

    def test_update_particle_throws(self):
        with self.assertRaises(Exception):
            self.pc.update_particle(self.particle_1)

    def test_update_particle(self):
        container = self.pc
        # add particles
        container.add_particle(self.particle_1)
        container.add_particle(self.particle_2)
        particle = Particle.from_particle(self.particle_1)
        particle.coordinates = (42, 42, 42)
        particle.data = 5
        container.update_particle(particle)
        updated_particle = container.get_particle(particle.uid)

        self.assertEqual(updated_particle, particle)
        self.assertNotEqual(particle, self.particle_1)

    def test_remove_particle(self):
        with self.assertRaises(ValueError):
            self.pc.remove_particle(0)

        particles = []
        for i in xrange(10):
            particles.append(Particle(
                uid=i, coordinates=(0.0, 0.0, 0.0)))

        for p in particles:
            self.pc.add_particle(p)

        for p in particles:
            self.pc.remove_particle(p.uid)

        for p in particles:
            with self.assertRaises(ValueError):
                self.pc.get_particle(p.uid)

        current = [p for p in self.pc.iter_particles()]
        self.assertFalse(current)

    def test_iter_particles(self):
        particles1 = [self.particle_1, self.particle_2]
        for particle in particles1:
            self.pc.add_particle(particle)

        # test iterating particles without giving ids
        particles2 = list(p for p in self.pc.iter_particles())
        self.compare_list(particles1, particles2, order_sensitive=False)

        # test iterating particles by giving ids
        particles1 = [self.particle_1, self.particle_2]
        ids1 = list(p.uid for p in particles1)
        particles2 = list(p for p in self.pc.iter_particles(ids1))
        self.compare_list(particles1, particles2)

        # test again with different order of ids
        particles1 = [self.particle_2, self.particle_1, self.particle_1]
        ids1 = list(p.uid for p in particles1)
        particles2 = list(p for p in self.pc.iter_particles(ids1))
        self.compare_list(particles1, particles2, order_sensitive=False)

    def test_add_get_bond(self):
        self.pc.add_bond(self.bond_1)
        bond = self.pc.get_bond(self.bond_1.uid)
        self.assertTrue(bond is not self.bond_1)
        self.assertEqual(bond, self.bond_1)

    def test_add_get_bond_with_default_id(self):
        b = Bond((1, 0))
        uid = self.pc.add_bond(b)
        bond = self.pc.get_bond(uid)
        self.assertTrue(bond is not b)
        self.assertEqual(bond.uid, uid)
        self.assertEqual(bond.particles, b.particles)

    def test_add_bond_with_same_id(self):
        self.pc.add_bond(self.bond_1)
        with self.assertRaises(Exception):
            self.pc.add_bond(self.bond_1)

    def test_has_bond_ok(self):
        self.pc.add_bond(self.bond_1)
        self.assertTrue(self.pc.has_bond(self.bond_1.uid))

    def test_has_bond_false(self):
        self.assertFalse(self.pc.has_bond(self.bond_1))

    def test_get_bond_throws(self):
        with self.assertRaises(Exception):
            self.pc.get_bond(0)

    def test_update_bond(self):
        with self.assertRaises(Exception):
            self.pc.update_bond(self.bond_1)

        self.pc.add_bond(self.bond_1)
        self.pc.add_bond(self.bond_2)
        b = copy.deepcopy(self.bond_1)
        b.particles = (1, 1)
        self.pc.update_bond(b)
        updated_b = self.pc.get_bond(b.uid)

        self.assertEqual(b, updated_b)
        self.assertNotEqual(b, self.bond_1)

    def test_remove_bond(self):
        with self.assertRaises(ValueError):
            self.pc.remove_bond(0)

        bonds = []
        for i in xrange(10):
            bonds.append(Bond(uid=i, particles=(0, 0)))

        for bond in bonds:
            self.pc.add_bond(bond)

        for bond in bonds:
            self.pc.remove_bond(bond.uid)

        for bond in bonds:
            with self.assertRaises(ValueError):
                self.pc.get_bond(bond.uid)


if __name__ == '__main__':
    unittest.main()
