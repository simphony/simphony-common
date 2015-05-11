import abc
import uuid
from functools import partial

from simphony.testing.utils import (
    create_data_container, create_points, compare_points, compare_elements,
    grouper, compare_data_containers)
from simphony.cuds.mesh import Point, Edge, Cell, Face
from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer


class MeshAttributesCheck(object):

    __metaclass__ = abc.ABCMeta

    supported_cuba = list(CUBA)

    def setUp(self):
        self.addTypeEqualityFunc(
            DataContainer, partial(compare_data_containers, testcase=self))

    @abc.abstractmethod
    def container_factory(self, name):
        """ Create and return the container object
        """

    def test_container_name(self):
        # when
        container = self.container_factory('my_name')
        # then
        self.assertEqual(container.name, 'my_name')

    def test_container_name_update(self):
        # given
        container = self.container_factory('my_name')

        # when
        container.name = 'new'

        # then
        self.assertEqual(container.name, 'new')

    def test_container_data(self):
        # when
        container = self.container_factory('my_name')
        # then
        self.assertEqual(container.data, DataContainer())

    def test_container_data_update(self):
        # given
        container = self.container_factory('my_name')
        data = create_data_container(restrict=self.supported_cuba)

        # when
        container.data = data

        # then
        self.assertEqual(container.data, data)
        self.assertIsNot(container.data, data)

    def test_container_data_update_with_unsupported_cuba(self):
        # given
        container = self.container_factory('my_name')
        data = create_data_container()
        expected_data = create_data_container(restrict=self.supported_cuba)

        # when
        container.data = data

        # then
        self.assertEqual(container.data, expected_data)
        self.assertIsNot(container.data, expected_data)


class MeshItemOperationsCheck(object):

    __metaclass__ = abc.ABCMeta

    supported_cuba = list(CUBA)
    operation_mapping = {
        'get item': 'none',
        'add item': 'none',
        'update item': 'none',
        'iter items': 'none'}

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

    def get_operation(self, container, *args, **kwrds):
        method = getattr(container, self.operation_mapping['get item'])
        return method(*args, **kwrds)

    def add_operation(self, container, *args, **kwrds):
        method = getattr(container, self.operation_mapping['add item'])
        return method(*args, **kwrds)

    def update_operation(self, container, *args, **kwrds):
        method = getattr(container, self.operation_mapping['update item'])
        return method(*args, **kwrds)

    def iter_operation(self, container, *args, **kwrds):
        method = getattr(container, self.operation_mapping['iter items'])
        return method(*args, **kwrds)

    def _add_items(self, container, items=None):
        items = items if items is not None else self.item_list
        return [self.add_operation(container, item) for item in items]

    def test_adding_and_getting_items(self):
        container = self.container

        # add items
        uids = self._add_items(container)

        # get items
        for index, expected in enumerate(self.item_list):
            self.assertEqual(
                self.get_operation(container, uids[index]), expected)

    def test_exception_on_get_item_with_wrong_uid(self):
        # given
        container = self.container
        invalid_uuid = uuid.uuid4()

        # when/then
        with self.assertRaises(KeyError):
            self.get_operation(container, invalid_uuid)

    def test_exception_on_get_item_with_invalid_uid(self):
        # given
        container = self.container
        invalid_uuid = None

        # when/then
        with self.assertRaises(TypeError):
            self.get_operation(container, invalid_uuid)

    def test_add_item_with_uid(self):
        # given
        container = self.container
        uid = uuid.uuid4()
        expected = self.create_item(uid)

        # when
        item_uid = self.add_operation(container, expected)

        # then
        self.assertEqual(item_uid, uid)
        self.assertEqual(self.get_operation(container, uid), expected)

    def test_add_item_with_unsuported_cuba(self):
        # given
        container = self.container
        expected = self.create_item(None)
        expected.data = create_data_container()

        # when
        uid = self.add_operation(container, expected)

        # then
        retrieved = self.get_operation(container, uid)
        expected.data = create_data_container(restrict=self.supported_cuba)
        self.assertEqual(retrieved, expected)

    def test_exception_when_adding_item_twice(self):
        # given
        container = self.container
        self._add_items(container)

        # when/then
        with self.assertRaises(ValueError):
            self.add_operation(container, self.item_list[3])

    def test_update_item_data(self):
        # given
        container = self.container
        uids = self._add_items(container)
        item = self.get_operation(container, uids[2])
        item.data = create_data_container(restrict=self.supported_cuba)

        # when
        self.update_operation(container, item)

        # then
        retrieved = self.get_operation(container, item.uid)
        self.assertEqual(retrieved, item)
        self.assertNotEqual(item, self.item_list[2])
        self.assertNotEqual(retrieved, self.item_list[2])

    def test_update_item_with_unsuported_cuba(self):
        # given
        container = self.container
        uids = self._add_items(container)
        item = self.get_operation(container, uids[2])
        item.data = create_data_container()

        # when
        self.update_operation(container, item)

        # then
        retrieved = self.get_operation(container, item.uid)
        item.data = create_data_container(restrict=self.supported_cuba)
        self.assertEqual(retrieved, item)

    def test_exception_when_update_item_with_wrong_id(self):
        # given
        container = self.container
        item = self.create_item(uuid.uuid4())

        # when/then
        with self.assertRaises(ValueError):
            self.update_operation(container, item)

    def test_snapshot_principle(self):
        # given
        container = self.container
        uid = uuid.uuid4()
        item = self.create_item(uid)
        self.add_operation(container, item)

        # when
        item.data = DataContainer()

        # then
        retrieved = self.get_operation(container, uid)
        self.assertNotEqual(retrieved, item)
        self.assertNotEqual(retrieved.data, item.data)

    def test_snapshot_principle_on_iteration(self):
        # given
        container = self.container
        uid = uuid.uuid4()
        item = self.create_item(uid)
        self.add_operation(container, item)

        # when
        item.data = DataContainer()

        # then
        retrieved = tuple(self.iter_operation(container))[0]
        self.assertNotEqual(retrieved, item)
        self.assertNotEqual(retrieved.data, item.data)

    def test_iterate_items_when_passing_ids(self):
        # given
        container = self.container
        self._add_items(container)
        items = [item for item in self.item_list[::2]]
        ids = [item.uid for item in items]

        # when
        iterated_items = [
            item for item in self.iter_operation(container, ids)]

        # then
        for item, reference in map(None, iterated_items, items):
            self.assertEqual(item, reference)

    def test_iterate_all_items(self):
        # given
        container = self.container
        self._add_items(container)
        items = {item.uid: item for item in self.item_list}

        # when
        iterated_items = [
            item for item in self.iter_operation(container)]

        # then
        # The order of iteration is not important in this case.
        self.assertEqual(len(items), len(iterated_items))
        for item in iterated_items:
            self.assertEqual(item, items[item.uid])

    def test_exception_on_iter_items_when_passing_wrong_ids(self):
        container = self.container
        self._add_items(container)
        ids = [item.uid for item in self.item_list]
        ids.append(uuid.UUID(int=20))
        with self.assertRaises(KeyError):
            for item in self.iter_operation(container, ids):
                pass
        self.assertEqual(item.uid, self.item_list[-1].uid)


class MeshPointOperationsCheck(MeshItemOperationsCheck):

    def setUp(self):
        MeshItemOperationsCheck.setUp(self)
        self.addTypeEqualityFunc(
            Point, partial(compare_points, testcase=self))

    def create_items(self):
        return create_points()

    def create_item(self, uid):
        return Point(
            uid=uid,
            coordinates=(0.1, -3.5, 44),
            data=create_data_container(restrict=self.supported_cuba))

    operation_mapping = {
        'get item': 'get_point',
        'add item': 'add_point',
        'update item': 'update_point',
        'iter items': 'iter_points'}

    def test_update_item_coordniates(self):
        # given
        container = self.container
        uids = self._add_items(container)
        item = self.get_operation(container, uids[2])
        item.coordinates = (123, 456, 789)

        # when
        self.update_operation(container, item)

        # then
        retrieved = self.get_operation(container, item.uid)
        self.assertEqual(retrieved, item)
        self.assertNotEqual(item, self.item_list[2])
        self.assertNotEqual(retrieved, self.item_list[2])


class MeshElementOperationsCheck(MeshItemOperationsCheck):

    operation_mapping = {
        'get item': 'none',
        'add item': 'none',
        'update item': 'none',
        'iter items': 'none',
        'has items': 'none'}

    points_range = None

    def has_items_operation(self, container, *args, **kwrds):
        method = getattr(container, self.operation_mapping['has items'])
        return method(*args, **kwrds)

    def test_has_items(self):
        container = self.container

        # container without items
        self.assertFalse(self.has_items_operation(container))

        # container with items
        self.add_operation(container, self.item_list[0])
        self.assertTrue(self.has_items_operation(container))

    def test_update_item_points(self):
        # given
        container = self.container
        uids = self._add_items(container)
        item = self.get_operation(container, uids[2])

        # increasing
        for n in self.points_range:
            # when
            item.points = tuple(uuid.uuid4() for _ in range(n))
            self.update_operation(container, item)

            # then
            retrieved = self.get_operation(container, item.uid)
            self.assertEqual(retrieved, item)
            self.assertNotEqual(item, self.item_list[2])
            self.assertNotEqual(retrieved, self.item_list[2])

        # decreasing
        for n in self.points_range[::-1]:
            # when
            item.points = tuple(uuid.uuid4() for _ in range(n))
            self.update_operation(container, item)

            # then
            retrieved = self.get_operation(container, item.uid)
            self.assertEqual(retrieved, item)
            self.assertNotEqual(item, self.item_list[2])
            self.assertNotEqual(retrieved, self.item_list[2])


class MeshEdgeOperationsCheck(MeshElementOperationsCheck):

    def setUp(self):
        MeshItemOperationsCheck.setUp(self)
        self.addTypeEqualityFunc(
            Edge, partial(compare_elements, testcase=self))

    operation_mapping = {
        'get item': 'get_edge',
        'add item': 'add_edge',
        'update item': 'update_edge',
        'iter items': 'iter_edges',
        'has items': 'has_edges'}

    points_range = [2]

    def create_items(self):
        uids = [uuid.uuid4() for _ in range(12)]
        return [Edge(
            points=puids,
            data=create_data_container(restrict=self.supported_cuba))
            for puids in grouper(uids, 2)]

    def create_item(self, uid):
        return Edge(
            uid=uid,
            points=[uuid.uuid4(), uuid.uuid4()],
            data=create_data_container(restrict=self.supported_cuba))


class MeshFaceOperationsCheck(MeshElementOperationsCheck):

    def setUp(self):
        MeshItemOperationsCheck.setUp(self)
        self.addTypeEqualityFunc(
            Face, partial(compare_elements, testcase=self))

    operation_mapping = {
        'get item': 'get_face',
        'add item': 'add_face',
        'update item': 'update_face',
        'iter items': 'iter_faces',
        'has items': 'has_faces'}

    points_range = [3, 4]

    def create_items(self):
        uids = [uuid.uuid4() for _ in range(32)]
        return [Face(
            points=puids,
            data=create_data_container(restrict=self.supported_cuba))
            for puids in grouper(uids, 3)]

    def create_item(self, uid):
        return Face(
            uid=uid,
            points=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4()],
            data=create_data_container(restrict=self.supported_cuba))


class MeshCellOperationsCheck(MeshElementOperationsCheck):

    def setUp(self):
        MeshItemOperationsCheck.setUp(self)
        self.addTypeEqualityFunc(
            Cell, partial(compare_elements, testcase=self))

    operation_mapping = {
        'get item': 'get_cell',
        'add item': 'add_cell',
        'update item': 'update_cell',
        'iter items': 'iter_cells',
        'has items': 'has_cells'}

    points_range = range(4, 8)

    def create_items(self):
        uids = [uuid.uuid4() for _ in range(32)]
        return [Cell(
            points=puids,
            data=create_data_container(restrict=self.supported_cuba))
            for puids in grouper(uids, 4)]

    def create_item(self, uid):
        return Cell(
            uid=uid,
            points=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4()],
            data=create_data_container(restrict=self.supported_cuba))