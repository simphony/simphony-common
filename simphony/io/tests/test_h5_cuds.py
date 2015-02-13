import unittest
import os

import tables
import uuid

from simphony.cuds.particles import Particle, ParticleContainer
from simphony.cuds.mesh import Point, Mesh
from simphony.io.h5_cuds import H5CUDS
from simphony.io.file_particle_container import FileParticleContainer
from simphony.io.file_mesh import FileMesh


class TestH5CUDS(unittest.TestCase):

    def setUp(self):
        # create some particles
        self.particles = []
        self.points = []
        for i in xrange(10):
            self.particles.append(Particle((1.1*i, 2.2*i, 3.3*i), uid=i))
            self.points.append(Point((1.1*i, 2.2*i, 3.3*i), uid=uuid.uuid4()))

        self.file_a = H5CUDS.open('test_A.cuds')
        self.file_b = H5CUDS.open('test_B.cuds')

    def tearDown(self):
        self.file_a.close()
        self.file_b.close()
        os.remove('test_A.cuds')
        os.remove('test_B.cuds')

    def test_init_with_append_mode(self):
        file = H5CUDS.open('test.cuds', mode='a')
        self.assertTrue(file.valid())
        file.close()
        os.remove('test.cuds')

    def test_init_with_write_mode(self):
        file = H5CUDS.open('test.cuds', mode='w')
        self.assertTrue(file.valid())
        file.close()
        os.remove('test.cuds')

    def test_init_with_unsupported_mode(self):
        with self.assertRaises(Exception):
            file = H5CUDS.open('test.cuds', mode='x')
            file.valid()

    def test_init_with_read_only_mode(self):
        file = H5CUDS.open('test.cuds', mode='w')
        file.close()

        with self.assertRaises(Exception):
            file = H5CUDS.open('test.cuds', mode='r')
        os.remove('test.cuds')

    def test_init_with_read_only_file(self):
        with tables.open_file('test.cuds', mode="w"):
            pass

        with tables.open_file('test.cuds', mode="r") as pfile:
            with self.assertRaises(Exception):
                H5CUDS(pfile)
        os.remove('test.cuds')

    def test_init_with_non_file(self):
        with self.assertRaises(Exception):
            H5CUDS(None)

    def test_valid(self):
        self.assertTrue(self.file_a.valid())
        self.file_a.close()
        self.assertFalse(self.file_a.valid())
        self.file_a = H5CUDS.open('test_A.cuds')
        self.assertTrue(self.file_a.valid())

    def test_get_missing_particle_container(self):
        with self.assertRaises(ValueError):
            self.file_a.get_particle_container('foo')

    def test_add_particle_container_empty(self):
        pc = self.file_a.add_particle_container(
            ParticleContainer(name="test"))
        self.assertEqual("test", pc.name)
        self.assertEqual(0, len(list(b for b in pc.iter_particles())))
        self.assertEqual(0, len(list(p for p in pc.iter_bonds())))

    def test_add_particle_container_with_same_name(self):
        self.file_a.add_particle_container(
            ParticleContainer(name="test"))
        with self.assertRaises(ValueError):
            self.file_a.add_particle_container(
                ParticleContainer(name="test"))

    def test_add_get_particle_container(self):
        # add particle container and add points to it
        pc_test_a = self.file_a.add_particle_container(
            ParticleContainer(name="test"))
        for p in self.particles:
            uid = pc_test_a.add_particle(p)
            self.assertEqual(p.uid, uid)
            self.assertEqual(
                p.coordinates, pc_test_a.get_particle(uid).coordinates)

        num_particles = len(list(p for p in pc_test_a.iter_particles()))
        self.assertEqual(num_particles, len(self.particles))

        # add the particle container from the first file
        # into the second file
        pc_test_b = self.file_b.add_particle_container(pc_test_a)

        for p in pc_test_a.iter_particles():
            p1 = pc_test_b.get_particle(p.uid)
            self.assertEqual(p1.uid, p.uid)
            self.assertEqual(p1.coordinates, p.coordinates)

        # close file and test if we can access it
        self.file_a.close()
        with self.assertRaises(Exception):
            pc_test_a.delete(self.particles[0].uid)
        with self.assertRaises(Exception):
            pc_closed_file = self.file_a.get_particle_container('test')
            pc_closed_file.delete(self.particles[0].uid)

        # reopen file (in append mode)
        self.file_a = H5CUDS.open('test_A.cuds')
        pc_test_a = self.file_a.get_particle_container('test')
        for p in self.particles:
            p1 = pc_test_a.get_particle(p.uid)
            self.assertEqual(p1.uid, p.uid)
            self.assertEqual(p1.coordinates, p.coordinates)

    def test_iter_particle_container(self):
        pc_names = []
        # add a few empty particle containers
        for i in xrange(5):
            name = "test_" + str(i)
            pc_names.append(name)
            self.file_a.add_particle_container(
                ParticleContainer(name=name))

        # test iterating over all
        names = list(
            pc.name for pc in self.file_a.iter_particle_containers())
        self.assertEquals(len(names), len(pc_names))
        for name in names:
            self.assertTrue(name in pc_names)

        # test iterating over a specific subset
        subset = pc_names[:3]
        names = list(
            pc.name for pc in self.file_a.iter_particle_containers(subset))
        self.assertEquals(names, subset)

        for pc in self.file_a.iter_particle_containers(pc_names):
            self.assertTrue(isinstance(pc, FileParticleContainer))

    def test_iter_particle_container_wrong(self):
        pc_names = ["wrong1", "wrong"]
        with self.assertRaises(ValueError):
            [pc for pc in self.file_a.iter_particle_containers(pc_names)]

    def test_delete_particle_container(self):
        pc_names = []

        # add a few empty particle containers
        for i in xrange(5):
            name = "test_" + str(i)
            pc_names.append(name)
            self.file_a.add_particle_container(
                ParticleContainer(name=name))

        # delete each of the particle containers
        for pc in self.file_a.iter_particle_containers():
            self.file_a.delete_particle_container(pc.name)

            # test that we can't get deleted container
            with self.assertRaises(ValueError):
                self.file_a.get_particle_container(pc.name)

            # test that we can't use the deleted container
            with self.assertRaises(Exception):
                pc.add_particle(self.particles[0])

    def test_delete_non_existing_particle_container(self):
        with self.assertRaises(ValueError):
            self.file_a.delete_particle_container("foo")

    def test_particle_container_rename(self):
        pc = self.file_a.add_particle_container(
            ParticleContainer(name="foo"))
        pc.name = "bar"
        self.assertEqual("bar", pc.name)

        # we should not be able to use the old name "foo"
        with self.assertRaises(ValueError):
            self.file_a.get_particle_container("foo")
        with self.assertRaises(ValueError):
            self.file_a.delete_particle_container("foo")
        with self.assertRaises(ValueError):
            [_ for _ in self.file_a.iter_particle_containers(names=["foo"])]

        # we should be able to access using the new "bar" name
        pc_bar = self.file_a.get_particle_container("bar")
        self.assertEqual("bar", pc_bar.name)

        # and we should be able to use the no-longer used
        # "foo" name when adding another particle container
        pc = self.file_a.add_particle_container(
            ParticleContainer(name="foo"))

    def test_get_missing_mesh(self):
        with self.assertRaises(ValueError):
            self.file_a.get_mesh('foo')

    def test_add_mesh_empty(self):
        m = self.file_a.add_mesh(Mesh(name="test"))
        self.assertEqual("test", m.name)
        self.assertEqual(0, len(list(p for p in m.iter_points())))
        self.assertEqual(0, len(list(e for e in m.iter_edges())))
        self.assertEqual(0, len(list(f for f in m.iter_faces())))
        self.assertEqual(0, len(list(c for c in m.iter_cells())))

    def test_add_mesh_with_same_name(self):
        self.file_a.add_mesh(Mesh(name="test"))
        with self.assertRaises(ValueError):
            self.file_a.add_mesh(Mesh(name="test"))

    def test_add_get_mesh(self):
        # add mesh and add points to it
        m_test_a = self.file_a.add_mesh(Mesh(name="test"))
        for p in self.points:
            uid = m_test_a.add_point(p)
            self.assertEqual(p.uid, uid)
            self.assertEqual(
                p.coordinates, m_test_a.get_point(uid).coordinates)

        num_points = len(list(p for p in m_test_a.iter_points()))
        self.assertEqual(num_points, len(self.points))

        # add the mesh from the first file into the second file
        m_test_b = self.file_b.add_mesh(m_test_a)

        for p in m_test_a.iter_points():
            p1 = m_test_b.get_point(p.uid)
            self.assertEqual(p1.uid, p.uid)
            self.assertEqual(p1.coordinates, p.coordinates)

        # close file and test if we can access it
        self.file_a.close()
        with self.assertRaises(Exception):
            m_test_a.delete(self.points[0].uid)
        with self.assertRaises(Exception):
            m_closed_file = self.file_a.get_mesh('test')
            m_closed_file.delete(self.points[0].uid)

        # reopen file (in append mode)
        self.file_a = H5CUDS.open('test_A.cuds')
        pc_test_a = self.file_a.get_mesh('test')
        for p in self.points:
            p1 = pc_test_a.get_point(p.uid)
            self.assertEqual(p1.uid, p.uid)
            self.assertEqual(p1.coordinates, p.coordinates)

    def test_iter_mesh(self):
        m_names = []
        # add a few empty mesh
        for i in xrange(5):
            name = "test_" + str(i)
            m_names.append(name)
            self.file_a.add_mesh(Mesh(name=name))

        # test iterating over all
        names = list(
            m.name for m in self.file_a.iter_meshes())
        self.assertEquals(len(names), len(m_names))
        for name in names:
            self.assertTrue(name in m_names)

        # test iterating over a specific subset
        subset = m_names[:3]
        names = list(
            m.name for m in self.file_a.iter_meshes(subset))
        self.assertEquals(names, subset)

        for m in self.file_a.iter_meshes(m_names):
            self.assertTrue(isinstance(m, FileMesh))

    def test_iter_mesh_wrong(self):
        m_names = ["wrong1", "wrong"]
        with self.assertRaises(ValueError):
            [m for m in self.file_a.iter_meshes(m_names)]

    def test_delete_mesh(self):
        m_names = []

        # add a few empty meshes
        for i in xrange(5):
            name = "test_" + str(i)
            m_names.append(name)
            self.file_a.add_mesh(Mesh(name=name))

        # delete each of the mesh
        for m in self.file_a.iter_meshes():
            self.file_a.delete_mesh(m.name)

            # test that we can't get deleted mesh
            with self.assertRaises(ValueError):
                self.file_a.get_mesh(m.name)

            # test that we can't use the deleted mesh
            with self.assertRaises(Exception):
                m.add_point(self.points[0])

    def test_delete_non_existing_mesh(self):
        with self.assertRaises(ValueError):
            self.file_a.delete_mesh("foo")

    def test_mesh_rename(self):
        m = self.file_a.add_mesh(Mesh(name="foo"))
        m.name = "bar"
        self.assertEqual("bar", m.name)

        # we should not be able to use the old name "foo"
        with self.assertRaises(ValueError):
            self.file_a.get_mesh("foo")
        with self.assertRaises(ValueError):
            self.file_a.delete_mesh("foo")
        with self.assertRaises(ValueError):
            [_ for _ in self.file_a.iter_meshes(names=["foo"])]

        # we should be able to access using the new "bar" name
        m_bar = self.file_a.get_mesh("bar")
        self.assertEqual("bar", m_bar.name)

        # and we should be able to use the no-longer used
        # "foo" name when adding another mesh
        m = self.file_a.add_mesh(Mesh(name="foo"))


if __name__ == '__main__':
    unittest.main()
