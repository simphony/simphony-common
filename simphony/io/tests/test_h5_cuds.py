import unittest
import os
from contextlib import closing
import shutil
import tempfile
import uuid

from simphony.cuds.particles import Particle, ParticleContainer
from simphony.cuds.mesh import Point, Mesh
from simphony.cuds.lattice import Lattice
from simphony.io.h5_cuds import H5CUDS
from simphony.io.file_mesh import FileMesh
from simphony.io.h5_particles import H5Particles


class TestH5CUDS(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.maxDiff = None
        # create some particles
        self.particles = []
        self.points = []
        for i in xrange(10):
            self.particles.append(
                Particle((1.1*i, 2.2*i, 3.3*i), uid=uuid.uuid4()))
            self.points.append(Point((1.1*i, 2.2*i, 3.3*i), uid=uuid.uuid4()))

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_open_with_append_mode(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename, 'a')) as handle:
            self.assertTrue(handle.valid())

    def test_open_with_write_mode(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename, 'w')) as handle:
            self.assertTrue(handle.valid())

    def test_open_with_read_only_mode(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename, 'w')) as handle:
            self.assertTrue(handle.valid())
        with closing(H5CUDS.open(filename, 'r')) as handle:
            self.assertTrue(handle.valid())

    def test_init_with_non_file(self):
        with self.assertRaises(Exception):
            H5CUDS(None)

    def test_valid(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename, 'w')) as handle:
            self.assertTrue(handle.valid())
        self.assertFalse(handle.valid())
        with closing(H5CUDS.open(filename, 'a')) as handle:
            self.assertTrue(handle.valid())
        self.assertFalse(handle.valid())

    def test_get_missing_particle_container(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            with self.assertRaises(ValueError):
                handle.get_particle_container('foo')

    def test_add_particle_container_empty(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            pc = handle.add_particle_container(ParticleContainer(name="test"))
            self.assertEqual("test", pc.name)
            self.assertEqual(0, sum(1 for _ in pc.iter_particles()))
            self.assertEqual(0, sum(1 for _ in pc.iter_bonds()))

    def test_add_particle_container_with_same_name(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            handle.add_particle_container(ParticleContainer(name="test"))
            with self.assertRaises(ValueError):
                handle.add_particle_container(
                    ParticleContainer(name="test"))

    def test_add_get_particle_container(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        filename_copy = os.path.join(self.temp_dir, 'test-copy.cuds')
        with closing(H5CUDS.open(filename, 'w')) as handle:
            # add particle container and add points to it
            pc_test = handle.add_particle_container(
                ParticleContainer(name="test"))
            for particle in self.particles:
                uid = pc_test.add_particle(particle)
                self.assertEqual(particle.uid, uid)
                self.assertEqual(
                    particle.coordinates,
                    pc_test.get_particle(uid).coordinates)
            self.assertEqual(
                len(self.particles), sum(1 for _ in pc_test.iter_particles()))

            # add the particle container from the first file
            # into the second file
            with closing(H5CUDS.open(filename_copy, 'w')) as handle_copy:
                pc_copy = handle_copy.add_particle_container(pc_test)

                for particle in pc_test.iter_particles():
                    particle_copy = pc_copy.get_particle(particle.uid)
                    self.assertEqual(particle_copy.uid, particle.uid)
                    self.assertEqual(
                        particle_copy.coordinates, particle.coordinates)

        with self.assertRaises(Exception):
            pc_test.delete(self.particles[0].uid)
        with self.assertRaises(Exception):
            handle.get_particle_container('test')

        # reopen file (in read only mode)
        with closing(H5CUDS.open(filename, 'r')) as handle:
            pc_test = handle.get_particle_container('test')
            for particles in self.particles:
                loaded = pc_test.get_particle(particle.uid)
                self.assertEqual(loaded.uid, particle.uid)
                self.assertEqual(loaded.coordinates, particle.coordinates)

    def test_iter_particle_container(self):
        # add a few empty particle containers
        pc_names = []
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            for i in xrange(5):
                name = "test_{}".format(i)
                pc_names.append(name)
                handle.add_particle_container(ParticleContainer(name=name))

            # test iterating over all
            names = [
                pc.name for pc in handle.iter_particle_containers()]
            self.assertEqual(names, pc_names)

            # test iterating over a specific subset
            subset = pc_names[:3]
            names = [
                pc.name for pc in handle.iter_particle_containers(subset)]
            self.assertEquals(names, subset)

            for pc in handle.iter_particle_containers(pc_names):
                self.assertTrue(isinstance(pc, H5Particles))

    def test_iter_particle_container_wrong(self):
        pc_names = ["wrong1", "wrong"]
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            with self.assertRaises(ValueError):
                [pc for pc in handle.iter_particle_containers(pc_names)]

    def test_delete_particle_container(self):
        pc_names = []

        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            # add a few empty particle containers
            for i in xrange(5):
                name = "test_" + str(i)
                pc_names.append(name)
                handle.add_particle_container(ParticleContainer(name=name))

            # delete each of the particle containers
            for pc in handle.iter_particle_containers():
                handle.delete_particle_container(pc.name)
                # test that we can't get deleted containers
                with self.assertRaises(ValueError):
                    handle.get_particle_container(pc.name)
                # test that we can't use the deleted container
                with self.assertRaises(Exception):
                    pc.add_particle(self.particles[0])

    def test_delete_non_existing_particle_container(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            with self.assertRaises(ValueError):
                handle.delete_particle_container("foo")

    def test_particle_container_rename(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            pc = handle.add_particle_container(
                ParticleContainer(name="foo"))
            pc.name = "bar"
            self.assertEqual("bar", pc.name)

            # we should not be able to use the old name "foo"
            with self.assertRaises(ValueError):
                handle.get_particle_container("foo")
            with self.assertRaises(ValueError):
                handle.delete_particle_container("foo")
            with self.assertRaises(ValueError):
                [_ for _ in handle.iter_particle_containers(names=["foo"])]

            # we should be able to access using the new "bar" name
            pc_bar = handle.get_particle_container("bar")
            self.assertEqual("bar", pc_bar.name)

            # and we should be able to use the no-longer used
            # "foo" name when adding another particle container
            pc = handle.add_particle_container(
                ParticleContainer(name="foo"))

    def test_get_missing_mesh(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            with self.assertRaises(ValueError):
                handle.get_mesh('foo')

    def test_add_mesh_empty(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            m = handle.add_mesh(Mesh(name="test"))
            self.assertEqual("test", m.name)
            self.assertEqual(0, len(list(p for p in m.iter_points())))
            self.assertEqual(0, len(list(e for e in m.iter_edges())))
            self.assertEqual(0, len(list(f for f in m.iter_faces())))
            self.assertEqual(0, len(list(c for c in m.iter_cells())))

    def test_add_mesh_with_same_name(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            handle.add_mesh(Mesh(name="test"))
            with self.assertRaises(ValueError):
                handle.add_mesh(Mesh(name="test"))

    def test_add_get_mesh(self):
        # add mesh and add points to it
        filename = os.path.join(self.temp_dir, 'test.cuds')
        filename_copy = os.path.join(self.temp_dir, 'test-copy.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            m_test = handle.add_mesh(Mesh(name="test"))
            for p in self.points:
                uid = m_test.add_point(p)
                self.assertEqual(p.uid, uid)
                self.assertEqual(
                    p.coordinates, m_test.get_point(uid).coordinates)

            num_points = sum(1 for _ in m_test.iter_points())
            self.assertEqual(num_points, len(self.points))

            # add the mesh from the first file into the second file
            with closing(H5CUDS.open(filename_copy)) as handle_copy:
                m_copy = handle_copy.add_mesh(m_test)

                for p in m_test.iter_points():
                    p1 = m_copy.get_point(p.uid)
                    self.assertEqual(p1.uid, p.uid)
                    self.assertEqual(p1.coordinates, p.coordinates)

        with self.assertRaises(Exception):
            m_test.delete(self.points[0].uid)
        with self.assertRaises(Exception):
            handle.get_mesh('test')

        # reopen file (in read only mode)
        with closing(H5CUDS.open(filename, 'r')) as handle:
            m_test = handle.get_mesh('test')
            for p in self.points:
                p1 = m_test.get_point(p.uid)
                self.assertEqual(p1.uid, p.uid)
                self.assertEqual(p1.coordinates, p.coordinates)

    def test_iter_mesh(self):
        m_names = []
        # add a few empty mesh
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            for i in xrange(5):
                name = "test_{}".format(i)
                m_names.append(name)
                handle.add_mesh(Mesh(name=name))

            # test iterating over all
            names = [
                m.name for m in handle.iter_meshes()]
            self.assertEqual(names, m_names)

            # test iterating over a specific subset
            subset = m_names[:3]
            names = [
                m.name for m in handle.iter_meshes(subset)]
            self.assertEqual(names, subset)

            for m in handle.iter_meshes():
                self.assertTrue(isinstance(m, FileMesh))

    def test_iter_mesh_wrong(self):
        m_names = ["wrong1", "wrong"]
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            with self.assertRaises(ValueError):
                [m for m in handle.iter_meshes(m_names)]

    def test_delete_mesh(self):
        m_names = []
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:

            # add a few empty meshes
            for i in xrange(5):
                name = "test_" + str(i)
                m_names.append(name)
                handle.add_mesh(Mesh(name=name))

            # delete each of the mesh
            for m in handle.iter_meshes():
                handle.delete_mesh(m.name)

            # test that we can't get deleted mesh
            with self.assertRaises(ValueError):
                handle.get_mesh(m.name)

            # test that we can't use the deleted mesh
            with self.assertRaises(Exception):
                m.add_point(self.points[0])

    def test_delete_non_existing_mesh(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            with self.assertRaises(ValueError):
                handle.delete_mesh("foo")

    def test_mesh_rename(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            m = handle.add_mesh(Mesh(name="foo"))
            m.name = "bar"
            self.assertEqual("bar", m.name)

            # we should not be able to use the old name "foo"
            with self.assertRaises(ValueError):
                handle.get_mesh("foo")
            with self.assertRaises(ValueError):
                handle.delete_mesh("foo")
            with self.assertRaises(ValueError):
                [_ for _ in handle.iter_meshes(names=["foo"])]

            # we should be able to access using the new "bar" name
            m_bar = handle.get_mesh("bar")
            self.assertEqual("bar", m_bar.name)

            # and we should be able to use the no-longer used
            # "foo" name when adding another mesh
            m = handle.add_mesh(Mesh(name="foo"))

    def test_add_get_delete_lattice(self):
        lat = Lattice('test_lattice', 'cubic', (1.0, 1.0, 1.0),
                      (2, 3, 4), (0.0, 0.0, 0.0))

        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename, 'w')) as handle:
            handle.add_lattice(lat)
            lat2 = handle.get_lattice('test_lattice')

            self.assertEqual(lat2.name, 'test_lattice')

            for N in lat2.iter_nodes():
                self.assertItemsEqual(N.data, lat.get_node(N.index).data)

            handle.delete_lattice('test_lattice')
            numlat = 0
            for N in handle.iter_lattices():
                numlat += 1
            self.assertEqual(numlat, 0)

    def test_iter_lattices(self):
        lat = Lattice('test_lattice', 'cubic', (1.0, 1.0, 1.0),
                      (2, 3, 4), (0.0, 0.0, 0.0))

        lat2 = Lattice('test_lattice2', 'cubic', (1.0, 1.0, 1.0),
                       (3, 3, 3), (0.0, 0.0, 0.0))

        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename, 'w')) as handle:
            handle.add_lattice(lat)
            handle.add_lattice(lat2)
            for lat in handle.iter_lattices():
                self.assertTrue(lat.name in ['test_lattice', 'test_lattice2'])


if __name__ == '__main__':
    unittest.main()
