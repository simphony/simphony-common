import abc
import uuid
import os
import sys
from contextlib import closing
import tempfile

from simphony.testing.utils import (  # noqa
    compare_particles_datasets, compare_mesh_datasets,
    compare_lattice_datasets)

from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer
from simphony.cuds.particles import Particle, Particles
from simphony.cuds.mesh import Point, Mesh
from simphony.cuds.lattice import Lattice
from simphony.io.h5_cuds import H5CUDS
from simphony.io.h5_mesh import H5Mesh
from simphony.io.h5_particles import H5Particles
from simphony.io.h5_lattice import H5Lattice


class CheckEngine(object):

    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.maxDiff = None
        self.items = self.create_dataset_items()

    @abc.abstractmethod
    def container_factory(self, name, mode='w'):
        """ Create and return the container object
        """

    @abc.abstractmethod
    def create_dataset(self, name):
        """ Create and return a cuds object
        """

    @abc.abstractmethod
    def create_dataset_items(self):
        """ Create and return a list of items
        """

    @abc.abstractmethod
    def check_instance_of_dataset(self, ds):
        """ Check if a dataset is instance of a class
        """

    operation_mapping = {
        'compare datasets': 'none',
        'add item': 'none'}

    def compare_operation(self, *args, **kwrds):
        method = getattr(
            sys.modules[__name__],
            self.operation_mapping['compare datasets'])
        return method(*args, **kwrds)

    def add_operation(self, container, *args, **kwrds):
        method = getattr(
            sys.modules[__name__],
            self.operation_mapping['add item'])
        return method(*args, **kwrds)

    def test_get_missing_dataset(self):
        with closing(self.container_factory('test.cuds')) as handle:
            with self.assertRaises(ValueError):
                handle.get_dataset('foo')

    def test_add_dataset_empty(self):
        with closing(self.container_factory('test.cuds')) as handle:
            reference = self.create_dataset(name='test')
            handle.add_dataset(reference)
            ds = handle.get_dataset("test")

            self.compare_operation(reference, ds, testcase=self)

    def test_add_dataset_empty_data(self):
        with closing(self.container_factory('test.cuds')) as handle:
            handle.add_dataset(self.create_dataset(name='test'))
            pc = handle.get_dataset("test")
            self.assertEqual(DataContainer(), pc.data)
            self.assertEqual(0, len(pc.data))

    def test_add_dataset_data_copy(self):
        with closing(self.container_factory('test.cuds')) as handle:
            handle.add_dataset(self.create_dataset(name='test'))
            pc = handle.get_dataset("test")
            data = pc.data
            data[CUBA.NAME] = 'somename'

            # Since the returned data is always a copy,
            #  therefore the pc.data should not have changed
            self.assertNotIn(CUBA.NAME, pc.data)
            # And the length should be still zero
            self.assertEqual(0, len(pc.data))
            pc.data = data
            # This time we replaced the pc.data,
            #  therefore it should have been changed
            self.assertIn(CUBA.NAME, pc.data)
            # The length also should have been changed
            self.assertEqual(1, len(pc.data))

    def test_add_get_dataset_data(self):
        original_ds = self.create_dataset(name='test')
        # Change data
        data = original_ds.data
        data[CUBA.NAME] = 'somename'
        original_ds.data = data

        # Store particle container along with its data
        with closing(self.container_factory('test.cuds')) as handle:
            ds = handle.add_dataset(original_ds)

        # Reopen the file and check the data if it is still there
        with closing(self.container_factory('test.cuds', 'r')) as handle:
            ds = handle.get_dataset('test')
            self.assertIn(CUBA.NAME, ds.data)
            self.assertEqual(ds.data[CUBA.NAME], 'somename')

    def test_add_dataset_with_same_name(self):
        filename = os.path.join(self.temp_dir, 'test.cuds')
        with closing(H5CUDS.open(filename)) as handle:
            handle.add_dataset(self.create_dataset(name='test'))
            with self.assertRaises(ValueError):
                handle.add_dataset(
                    self.create_dataset(name='test'))

    def test_iter_dataset(self):
        # add a few empty particle containers
        ds_names = []
        with closing(self.container_factory('test.cuds')) as handle:
            for i in xrange(5):
                name = "test_{}".format(i)
                ds_names.append(name)
                handle.add_dataset(self.create_dataset(name=name))

            # test iterating over all
            names = [
                ds.name for ds in handle.iter_datasets()]
            self.assertEqual(names, ds_names)

            # test iterating over a specific subset
            subset = ds_names[:3]
            names = [
                ds.name for ds in handle.iter_datasets(subset)]
            self.assertEquals(names, subset)

            for ds in handle.iter_datasets(ds_names):
                self.check_instance_of_dataset(ds)

    def test_iter_dataset_wrong(self):
        ds_names = ["wrong1", "wrong"]
        with closing(self.container_factory('test.cuds')) as handle:
            with self.assertRaises(ValueError):
                [ds for ds in handle.iter_datasets(ds_names)]

    def test_delete_dataset(self):
        with closing(self.container_factory('test.cuds')) as handle:
            # add a few empty particle containers
            for i in xrange(5):
                name = "test_" + str(i)
                handle.add_dataset(Particles(name=name))

            # delete each of the particle containers
            for ds in handle.iter_datasets():
                handle.remove_dataset(ds.name)
                # test that we can't get deleted containers
                with self.assertRaises(ValueError):
                    handle.get_dataset(ds.name)
                # test that we can't use the deleted container
                with self.assertRaises(Exception):
                    self.compare_operation(ds, self.items[0])

    def test_delete_non_existing_dataset(self):
        with closing(self.container_factory('test.cuds')) as handle:
            with self.assertRaises(ValueError):
                handle.remove_dataset("foo")

    def test_dataset_rename(self):
        with closing(self.container_factory('test.cuds')) as handle:
            handle.add_dataset(self.create_dataset(name='foo'))
            ds = handle.get_dataset("foo")
            ds.name = "bar"
            self.assertEqual("bar", ds.name)

            # we should not be able to use the old name "foo"
            with self.assertRaises(ValueError):
                handle.get_dataset("foo")
            with self.assertRaises(ValueError):
                handle.remove_dataset("foo")
            with self.assertRaises(ValueError):
                [_ for _ in handle.iter_datasets(names=["foo"])]

            # we should be able to access using the new "bar" name
            ds_bar = handle.get_dataset("bar")
            self.assertEqual("bar", ds_bar.name)

            # and we should be able to use the no-longer used
            # "foo" name when adding another particle container
            ds = handle.add_dataset(self.create_dataset(name='foo'))


class ParticlesCudsCheck(CheckEngine):

    operation_mapping = {
        'compare datasets': 'compare_particles_datasets',
        'add item': 'add_particle'}

    def create_dataset(self, name):
        """ Create and return a cuds object

        """
        return Particles(name=name)

    def create_dataset_items(self):
        """ Create and return a list of items
        """
        items = []
        for i in xrange(10):
            items.append(
                Particle((1.1*i, 2.2*i, 3.3*i), uid=uuid.uuid4()))
        return items

    def check_instance_of_dataset(self, ds):
        """ Check if a dataset is instance of a class
        """

        self.assertTrue(isinstance(ds, H5Particles))

    def test_add_get_dataset(self):
        with closing(self.container_factory('test.cuds')) as handle:
            # add particle container and add points to it
            handle.add_dataset(self.create_dataset(name='test'))
            ds_test = handle.get_dataset('test')
            for particle in self.items:
                uid = ds_test.add_particles([particle])
                self.assertEqual(particle.uid, uid[0])
                self.assertEqual(
                    particle.coordinates,
                    ds_test.get_particle(uid[0]).coordinates)
            self.assertEqual(
                len(self.items), sum(1 for _ in ds_test.iter_particles()))

            # add the particle container from the first file
            # into the second file
            with closing(
                    self.container_factory('test-copy.cuds')) as handle_copy:
                handle_copy.add_dataset(ds_test)
                ds_copy = handle_copy.get_dataset('test')

                for particle in ds_test.iter_particles():
                    particle_copy = ds_copy.get_particle(particle.uid)
                    self.assertEqual(particle_copy.uid, particle.uid)
                    self.assertEqual(
                        particle_copy.coordinates, particle.coordinates)

        with self.assertRaises(Exception):
            ds_test.delete(self.items[0].uid)
        with self.assertRaises(Exception):
            handle.get_dataset('test')

        # reopen file (in read only mode)
        with closing(self.container_factory('test.cuds', 'r')) as handle:
            ds_test = handle.get_dataset('test')
            for particles in self.items:
                loaded = ds_test.get_particle(particle.uid)
                self.assertEqual(loaded.uid, particle.uid)
                self.assertEqual(loaded.coordinates, particle.coordinates)


class MeshCudsCheck(CheckEngine):

    operation_mapping = {
        'compare datasets': 'compare_mesh_datasets',
        'add item': 'add_point'}

    def create_dataset(self, name):
        """ Create and return a cuds object

        """
        return Mesh(name=name)

    def create_dataset_items(self):
        """ Create and return a list of items
        """
        items = []
        for i in xrange(10):
            items.append(
                Point((1.1*i, 2.2*i, 3.3*i), uid=uuid.uuid4()))
        return items

    def check_instance_of_dataset(self, ds):
        """ Check if a dataset is instance of a class
        """

        self.assertTrue(isinstance(ds, H5Mesh))

    def test_add_get_mesh(self):
        # add mesh and add points to it
        with closing(self.container_factory('test.cuds')) as handle:
            handle.add_dataset(Mesh(name="test"))
            ds_test = handle.get_dataset("test")
            for p in self.items:
                uid = ds_test.add_point(p)
                self.assertEqual(p.uid, uid)
                self.assertEqual(
                    p.coordinates, ds_test.get_point(uid).coordinates)

            num_points = sum(1 for _ in ds_test.iter_points())
            self.assertEqual(num_points, len(self.items))

            # add the mesh from the first file into the second file
            with closing(
                    self.container_factory('test-copy.cuds')) as handle_copy:
                handle_copy.add_dataset(ds_test)
                ds_copy = handle.get_dataset("test")

                for p in ds_test.iter_points():
                    p1 = ds_copy.get_point(p.uid)
                    self.assertEqual(p1.uid, p.uid)
                    self.assertEqual(p1.coordinates, p.coordinates)

        with self.assertRaises(Exception):
            ds_test.delete(self.items[0].uid)
        with self.assertRaises(Exception):
            handle.get_dataset('test')

        # reopen file (in read only mode)
        with closing(self.container_factory('test.cuds', 'r')) as handle:
            ds_test = handle.get_dataset('test')
            for p in self.items:
                p1 = ds_test.get_point(p.uid)
                self.assertEqual(p1.uid, p.uid)
                self.assertEqual(p1.coordinates, p.coordinates)


class LatticeCudsCheck(CheckEngine):

    operation_mapping = {
        'compare datasets': 'compare_lattice_datasets',
        'add item': 'add'}

    def create_dataset(self, name):
        """ Create and return a cuds object

        """
        return Lattice(
            name, 'cubic', (1.0, 1.0, 1.0),
            (2, 3, 4), (0.0, 0.0, 0.0))

    def create_dataset_items(self):
        """ Create and return a list of items
        """
        items = []
        for i in xrange(10):
            items.append(
                Point((1.1*i, 2.2*i, 3.3*i), uid=uuid.uuid4()))
        return items

    def check_instance_of_dataset(self, ds):
        """ Check if a dataset is instance of a class
        """

        self.assertTrue(isinstance(ds, H5Lattice))
