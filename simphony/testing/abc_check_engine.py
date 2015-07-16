import abc
import uuid
import sys

from simphony.testing.utils import (  # noqa
    compare_particles_datasets, compare_mesh_datasets,
    compare_lattice_datasets)

from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer
from simphony.cuds.particles import Particle, Particles
from simphony.cuds.mesh import Point, Mesh
from simphony.cuds.lattice import Lattice


class CheckEngine(object):

    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self.items = self.create_dataset_items()

    @abc.abstractmethod
    def engine_factory(self):
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
        handle = self.engine_factory()
        with self.assertRaises(ValueError):
            handle.get_dataset('foo')

    def test_add_dataset(self):
        handle = self.engine_factory()
        reference = self.create_dataset(name='test')
        handle.add_dataset(reference)
        ds = handle.get_dataset("test")

        self.compare_operation(reference, ds, testcase=self)

    def test_add_dataset_data_copy(self):
        handle = self.engine_factory()

        reference = self.create_dataset(name='test')

        reference_data = reference.data
        reference_data[CUBA.NAME] = 'foo_name'
        reference.data = data

        handle.add_dataset(reference)

        ds = handle.get_dataset('test')
        
        data = ds.data
        data[CUBA.NAME] = 'somename'
        data[CUBA.MATERIAL] = 'foo_mat'

        # Since the returned data is always a copy,
        #  therefore the ds.data should not have changed
        self.assertNotEqual(reference,data[CUBA.NAME], ds.data[CUBA.NAME])
        self.assertNotIn(CUBA.MATERIAL, ds.data)
        # And the length should be still one
        self.assertEqual(1, len(ds.data))

        ds.data = data
        # This time we replaced the ds.data,
        #  therefore it should have been changed
        self.assertEqual(reference,data[CUBA.NAME], ds.data[CUBA.NAME])
        self.assertIn(CUBA.MATERIAL, ds.data)
        # The length also should have been changed
        self.assertEqual(2, len(ds.data))

    def test_add_get_dataset(self):
        handle = self.engine_factory()
        reference = self.create_dataset(name='test')

        # Store dataset container along with its data
        handle.add_dataset(reference)
        ds = handle.get_dataset('test')

        self.compare_operation(reference, ds, testcase=self)

    def test_add_get_dataset_data(self):
        handle = self.engine_factory()

        reference = self.create_dataset(name='test')
        # Change data
        data = reference.data
        data[CUBA.NAME] = 'somename'
        reference.data = data

        # Store dataset container along with its data
        handle.add_dataset(reference)
        ds = handle.get_dataset('test')

        self.compare_operation(reference, ds, testcase=self)

    def test_add_dataset_with_same_name(self):
        handle = self.engine_factory()
        handle.add_dataset(self.create_dataset(name='test'))
        with self.assertRaises(ValueError):
            handle.add_dataset(
                self.create_dataset(name='test'))

    def test_iter_dataset(self):
        handle = self.engine_factory()
        # add a few empty particle containers
        ds_names = []

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
        handle = self.engine_factory()
        ds_names = ["wrong1", "wrong"]

        with self.assertRaises(ValueError):
            [ds for ds in handle.iter_datasets(ds_names)]

    def test_delete_dataset(self):
        handle = self.engine_factory()
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
        handle = self.engine_factory()
        with self.assertRaises(ValueError):
            handle.remove_dataset("foo")

    def test_dataset_rename(self):
        handle = self.engine_factory()
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

    def setUp(self):
        CheckEngine.setUp(self)

    operation_mapping = {
        'compare datasets': 'compare_particles_datasets'}

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


class MeshCudsCheck(CheckEngine):

    def setUp(self):
        CheckEngine.setUp(self)

    operation_mapping = {
        'compare datasets': 'compare_mesh_datasets'}

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


class LatticeCudsCheck(CheckEngine):

    def setUp(self):
        CheckEngine.setUp(self)

    operation_mapping = {
        'compare datasets': 'compare_lattice_datasets'}

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
