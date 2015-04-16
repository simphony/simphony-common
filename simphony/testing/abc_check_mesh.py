import abc
import uuid
from functools import partial

from simphony.testing.utils import (
    create_data_container, create_points, compare_points)
from simphony.cuds.mesh import Point, Element
from simphony.core.data_container import DataContainer


class MeshItemOperationsCheck(object):

    __metaclass__ = abc.ABCMeta

    supported_cuba = CUBA

    def setUp(self):
        self.item_list = self.create_items()
        self.container = self.container_factory('foo')

    @abc.abstractmethod
    def create_items(self):
        """ Create and return a list of items

        """
    @abc.abstractmethod
    def create_item(self, uid):
        """ Create an item with the provided uid

        """

    @abc.abstractmethod
    def container_factory(self, name):
        """ Create and return the container object
        """

    def _add_items(self, container, items=None):
        items = items if items is not None else self._item_list
        return [container.add_item(item) for item in items]

    def test_has_item(self):
        container = self.container

        # container without items
        self.assertFalse(container.has_items())

        # container with items
        container.add_item(self.item_list[0])
        self.assertTrue(container.has_items())

    def test_adding_and_getting_items(self):
        container = self.container

        # add items
        uids = self._add_items(container)
        self.assertTrue(container.has_items())

        # get items
        for index, expected in enumerate(self.item_list):
            self.assertEqual(container.get_item(uids[index]), expected)

    def test_add_item_with_uid(self):
        container = self.container
        uid = uuid.uuid4()
        expected = self.create_item(uid)
        item_uid = container.add_item(expected)
        self.assertEqual(item_uid, uid)
        self.assertEqual(container.get_item(uid))

    def test_exception_when_adding_item_twice(self):
        container = self.container
        with self.assertRaises(ValueError):
            container.add_item(self.item_list[3])

    def test_update_item_data(self):
        container = self.container
        item = container.get_item(self.ids[2])
        item.data = create_data_container(restrict=self.supported_cuba)
        container.update_item(item)
        retrieved = container.get_item(item.uid)
        self.assertEqual(retrieved, item)

    def test_exception_when_update_item_when_wrong_id(self):
        container = self.container
        item = self.create_itme(uuid.uuid4())
        with self.assertRaises(ValueError):
            container.update_item(item)
        item = self.create_item(None)
        with self.assertRaises(ValueError):
            container.update_item(item)

    def test_iterate_items_when_passing_ids(self):
        items = [item for item in self.item_list[::2]]
        ids = [item.uid for item in items]
        iterated_items = [
            item for item in self.container.iter_items(ids)]
        for item, reference in map(None, iterated_items, items):
            self.assertEqual(item, reference)

    def test_iterate_all_items(self):
        items = {item.uid: item for item in self.item_list}
        iterated_items = [
            item for item in self.container.iter_items()]
        # The order of iteration is not important in this case.
        self.assertEqual(len(items), len(iterated_items))
        for item in iterated_items:
            self.assertEqual(item, items[item.uid])

    def test_exception_on_iter_items_when_passing_wrong_ids(self):
        ids = [item.uid for item in self.item_list]
        ids.append(uuid.UUID(int=20))
        with self.assertRaises(KeyError):
            for item in self.container.iter_items(ids):
                pass
        self.assertEqual(item.uid, self.item_list[-1].uid)


class MeshPointOperationsCheck(MeshItemOperationsCheck):

    def setUp(self):
        MeshItemOperationsCheck.setup(self)
        self.addTypeEqualityFunc(
            Point, partial(compare_points, testcase=self))

    def create_items(self):
        return create_points()

    def create_item(self, uid):
        return Point(
            uid=uid,
            coordinates=(0.1, -3.5, 44),
            data=create_data_container(restrict=self.supported_cuba))

    def test_update_item_coordinates(self):
        container = self.container
        item = container.get_item(self.ids[2])
        item.coordinates = (123, 456, 789)
        container.update_item(item)
        retrieved = container.get_item(item.uid)
        self.assertEqual(retrieved, item)


class MeshElementOperationsCheck(MeshItemOperationsCheck):

    def setUp(self):
        MeshItemOperationsCheck.setup(self)
        self.addTypeEqualityFunc(
            Element, partial(compare_element, testcase=self))

    def test_update_item_connections(self):
        container = self.container
        item = container.get_item(self.ids[2])
        item.points = self.create_item().points
        container.update_item(item)
        retrieved = container.get_item(item.uid)
        self.assertEqual(retrieved, item)
