import abc
import uuid
import random
from functools import partial

from .utils import (
    create_data_container, create_points, compare_points, compare_elements,
    grouper, compare_data_containers)
from ..cuds.mesh_items import Edge, Face, Cell, Point
from ..core import CUBA
from ..core.data_container import DataContainer


class CheckMeshContainer(object):

    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self.addTypeEqualityFunc(
            DataContainer, partial(compare_data_containers, testcase=self))

    @abc.abstractmethod
    def container_factory(self, name):
        """ Create and return the container object
        """

    @abc.abstractmethod
    def supported_cuba(self):
        """ Return a list of CUBA keys to use for restricted containers.
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
        data = create_data_container(restrict=self.supported_cuba())

        # when
        container.data = data

        # then
        self.assertEqual(container.data, data)
        self.assertIsNot(container.data, data)

    def test_container_data_update_with_unsupported_cuba(self):
        # given
        container = self.container_factory('my_name')
        data = create_data_container()
        expected_data = create_data_container(restrict=self.supported_cuba())

        # when
        container.data = data

        # then
        self.assertEqual(container.data, expected_data)
        self.assertIsNot(container.data, expected_data)


class CheckMeshItemOperations(object):

    __metaclass__ = abc.ABCMeta

    operation_mapping = {
        'get item': 'get',
        'add item': 'add',
        'update item': 'update',
        'iter items': 'iter',
        'has items': 'has_type',
        'count items': 'count_of'}

    def setUp(self):
        self.item_list = self.create_items()
        self.container = self.container_factory('foo')

    @abc.abstractmethod
    def supported_cuba(self):
        """ Return a list of CUBA keys to use for restricted containers.
        """

    @abc.abstractmethod
    def create_items(self):
        """ Create and return a list of items

        """
    @abc.abstractmethod
    def create_item(self, uid):
        """ Create an item with the provided uid

        """

    @abc.abstractproperty
    def item_type(self):
        """
        The item type this subclass handles
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
        return self.add_operation(container, items)

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
        item_uid = self.add_operation(container, [expected])

        # then
        self.assertEqual(item_uid, [uid])
        self.assertEqual(self.get_operation(container, uid), expected)

    def test_add_multiple_item_with_uid(self):
        # given
        container = self.container
        uida = uuid.uuid4()
        uidb = uuid.uuid4()
        expecteda = self.create_item(uida)
        expectedb = self.create_item(uidb)

        # when
        item_uid = self.add_operation(container, [expecteda, expectedb])

        # then
        self.assertEqual(item_uid, [uida, uidb])
        self.assertEqual(self.get_operation(container, uida), expecteda)
        self.assertEqual(self.get_operation(container, uidb), expectedb)

    def test_add_item_with_unsuported_cuba(self):
        # given
        container = self.container
        expected = self.create_item(None)
        expected.data = create_data_container()

        # when
        uid = self.add_operation(container, [expected])

        # then
        retrieved = self.get_operation(container, uid[0])
        expected.data = create_data_container(restrict=self.supported_cuba())
        self.assertEqual(retrieved, expected)

    def test_add_multiple_item_with_unsuported_cuba(self):
        # given
        container = self.container
        expecteda = self.create_item(None)
        expectedb = self.create_item(None)
        expecteda.data = create_data_container()
        expectedb.data = create_data_container()

        # when
        uid = self.add_operation(container, [expecteda, expectedb])

        # then
        retrieveda = self.get_operation(container, uid[0])
        expecteda.data = create_data_container(restrict=self.supported_cuba())
        self.assertEqual(retrieveda, expecteda)
        retrievedb = self.get_operation(container, uid[1])
        expectedb.data = create_data_container(restrict=self.supported_cuba())
        self.assertEqual(retrievedb, expectedb)

    def test_exception_when_adding_item_twice(self):
        # given
        container = self.container
        self._add_items(container)

        # when/then
        with self.assertRaises(ValueError):
            self.add_operation(container, [self.item_list[3]])

    def test_update_item_data(self):
        # given
        container = self.container
        uids = self._add_items(container)
        item = self.get_operation(container, uids[2])
        item.data = create_data_container(restrict=self.supported_cuba())

        # when
        self.update_operation(container, [item])

        # then
        retrieved = self.get_operation(container, item.uid)
        self.assertEqual(retrieved, item)
        self.assertNotEqual(item, self.item_list[2])
        self.assertNotEqual(retrieved, self.item_list[2])

    def test_update_multiple_item_data(self):
        # given
        container = self.container
        self._add_items(container)
        items = list(self.iter_operation(container, item_type=self.item_type))
        for item in items:
            item.data = create_data_container(restrict=self.supported_cuba())

        # when
        self.update_operation(container, items)

        # then
        for item in items:
            retrieved = self.get_operation(container, item.uid)
            self.assertEqual(retrieved, item)

    def test_update_item_with_unsuported_cuba(self):
        # given
        container = self.container
        uids = self._add_items(container)
        item = self.get_operation(container, uids[2])
        item.data = create_data_container()

        # when
        self.update_operation(container, [item])

        # then
        retrieved = self.get_operation(container, item.uid)
        item.data = create_data_container(restrict=self.supported_cuba())
        self.assertEqual(retrieved, item)

    def test_update_multiple_item_with_unsuported_cuba(self):
        # given
        container = self.container
        self._add_items(container)
        items = list(self.iter_operation(container, item_type=self.item_type))
        for item in items:
            item.data = create_data_container()

        # when
        self.update_operation(container, items)

        # then
        for item in items:
            retrieved = self.get_operation(container, item.uid)
            item.data = create_data_container(restrict=self.supported_cuba())
            self.assertEqual(retrieved, item)

    def test_exception_when_update_item_with_wrong_id(self):
        # given
        container = self.container
        item = self.create_item(uuid.uuid4())

        # when/then
        with self.assertRaises(ValueError):
            self.update_operation(container, [item])

    def test_exception_when_update_multiple_item_with_wrong_id(self):
        # given
        container = self.container
        items = [
            self.create_item(uuid.uuid4()),
            self.create_item(uuid.uuid4())
            ]

        # when/then
        with self.assertRaises(ValueError):
            self.update_operation(container, items)

    def test_snapshot_principle(self):
        # given
        container = self.container
        uid = uuid.uuid4()
        item = self.create_item(uid)
        self.add_operation(container, [item])

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
        self.add_operation(container, [item])

        # when
        item.data = DataContainer()

        # then
        retrieved = tuple(self.iter_operation(container,
                                              item_type=self.item_type))[0]
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

    def test_iterate_items_when_passing_ids_and_types(self):
        # given
        container = self.container
        self._add_items(container)
        items = [item for item in self.item_list[::2]]
        ids = [item.uid for item in items]

        # when
        iterated_items = [
            item for item in self.iter_operation(container,
                                                 ids,
                                                 item_type=self.item_type)]

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
            item for item in self.iter_operation(container,
                                                 item_type=self.item_type)]

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

    def test_container_data_and_item_data_conflict(self):
        # given
        container = self.container
        uids = self._add_items(container)

        # when
        container.data = DataContainer()

        # then
        for index, expected in enumerate(self.item_list):
            self.assertEqual(
                self.get_operation(container, uids[index]), expected)
        self.assertEqual(container.data, DataContainer())

    def test_contains(self):
        container = self.container
        self.assertFalse(uuid.uuid4() in self.container)

        uids = self._add_items(container)
        for uid in uids:
            self.assertTrue(uid in self.container)


class CheckMeshPointOperations(CheckMeshItemOperations):

    def setUp(self):
        CheckMeshItemOperations.setUp(self)
        self.addTypeEqualityFunc(
            Point, partial(compare_points, testcase=self))

    def create_items(self):
        return create_points(restrict=self.supported_cuba())

    def create_item(self, uid):
        return Point(
            uid=uid,
            coordinates=(0.1, -3.5, 44),
            data=create_data_container(restrict=self.supported_cuba()))

    @property
    def item_type(self):
        return CUBA.POINT

    def count_items_operation(self, container, *args, **kwrds):
        method = getattr(container, self.operation_mapping['count items'])
        return method(*args, **kwrds)

    def test_count_items(self):
        container = self.container

        # container without items
        self.assertEqual(
            self.count_items_operation(container, CUBA.POINT),
            0
        )

        # container with items
        num_items = len(self.item_list)
        self.add_operation(container, self.item_list)

        self.assertEqual(
            self.count_items_operation(container, CUBA.POINT),
            num_items
        )

    def test_length(self):
        container = self.container

        total = sum(
            self.count_items_operation(container, x)
            for x in [
                CUBA.POINT, CUBA.EDGE, CUBA.FACE, CUBA.CELL]
        )
        self.assertEqual(len(container), total)

    def test_count_items_with_unsupported_item(self):
        container = self.container

        # container without items
        with self.assertRaises(ValueError):
            self.count_items_operation(container, CUBA.NODE)

    def test_update_item_coordniates(self):
        # given
        container = self.container
        uids = self._add_items(container)
        item = self.get_operation(container, uids[2])
        item.coordinates = (123, 456, 789)

        # when
        self.update_operation(container, [item])

        # then
        retrieved = self.get_operation(container, item.uid)
        self.assertEqual(retrieved, item)
        self.assertNotEqual(item, self.item_list[2])
        self.assertNotEqual(retrieved, self.item_list[2])

    def test_update_multiple_item_coordniates(self):
        # given
        container = self.container
        uids = self._add_items(container)
        itema = self.get_operation(container, uids[1])
        itemb = self.get_operation(container, uids[2])
        itema.coordinates = (123, 456, 789)
        itemb.coordinates = (147, 258, 369)

        # when
        self.update_operation(container, [itema, itemb])

        # then
        retrieveda = self.get_operation(container, itema.uid)
        retrievedb = self.get_operation(container, itemb.uid)
        self.assertEqual(retrieveda, itema)
        self.assertEqual(retrievedb, itemb)
        self.assertNotEqual(itema, self.item_list[1])
        self.assertNotEqual(retrieveda, self.item_list[1])
        self.assertNotEqual(itemb, self.item_list[2])
        self.assertNotEqual(retrievedb, self.item_list[2])


class CheckMeshElementOperations(CheckMeshItemOperations):

    def setUp(self):
        self.points = []
        for multiplier in self.point_groups:
            points = create_points(restrict=self.supported_cuba())
            for point in points:
                point.coordinates = [
                    value * multiplier for value in point.coordinates]
            self.points += points
        self.uids = [uuid.uuid4() for _ in self.points]
        for uid, point in zip(self.uids, self.points):
            point.uid = uid
        CheckMeshItemOperations.setUp(self)
        self.container.add(self.points)

    points_range = None

    point_groups = [1]

    def has_items_operation(self, container, *args, **kwrds):
        method = getattr(container, self.operation_mapping['has items'])
        return method(*args, **kwrds)

    def count_items_operation(self, container, *args, **kwrds):
        method = getattr(container, self.operation_mapping['count items'])
        return method(*args, **kwrds)

    def test_has_items(self):
        container = self.container

        # container without items
        self.assertFalse(self.has_items_operation(container,
                                                  item_type=self.item_type))

        # container with items
        self.add_operation(container, [self.item_list[0]])
        self.assertTrue(self.has_items_operation(container,
                                                 item_type=self.item_type))

    def test_count_items(self):
        container = self.container

        # container without items
        self.assertEqual(
            self.count_items_operation(container, self.item_type),
            0
        )
        # container with items
        num_items = len(self.item_list)
        self.add_operation(container, self.item_list)

        self.assertEqual(
            self.count_items_operation(container, self.item_type),
            num_items
        )

    def test_count_items_with_unsupported_item(self):
        container = self.container

        # container without items
        with self.assertRaises(ValueError):
            self.count_items_operation(container, CUBA.NODE)

    def test_update_item_points(self):
        # given
        container = self.container
        uids = self._add_items(container)
        item = self.get_operation(container, uids[2])
        point_uids = container.add([
            Point((1.0 * i, 1.0 * i, 1.0 * i))
            for i in range(self.points_range[-1])])

        # increasing
        for n in self.points_range:
            # when
            item.points = tuple(point_uids[:n])
            self.update_operation(container, [item])

            # then
            retrieved = self.get_operation(container, item.uid)
            self.assertEqual(retrieved, item)
            self.assertNotEqual(item, self.item_list[2])
            self.assertNotEqual(retrieved, self.item_list[2])

        # decreasing
        for n in self.points_range[::-1]:
            # when
            item.points = tuple(point_uids[:n])
            self.update_operation(container, [item])

            # then
            retrieved = self.get_operation(container, item.uid)
            self.assertEqual(retrieved, item)
            self.assertNotEqual(item, self.item_list[2])
            self.assertNotEqual(retrieved, self.item_list[2])

    def test_update_multiple_items_points(self):
        # given
        container = self.container
        self._add_items(container)
        items = [
            i for i in self.iter_operation(container,
                                           item_type=self.item_type)]

        point_uids = container.add([
            Point((1.0 * i, 1.0 * i, 1.0 * i))
            for i in range(self.points_range[-1])])

        # increasing
        for n in self.points_range:
            # when
            for item in items:
                item.points = tuple(point_uids[:n])
            self.update_operation(container, items)

            # then
            for item in items:
                retrieved = self.get_operation(container, item.uid)
                self.assertEqual(retrieved, item)
                self.assertNotEqual(item, self.item_list[2])
                self.assertNotEqual(retrieved, self.item_list[2])

        # decreasing
        for n in self.points_range[::-1]:
            # when
            for item in items:
                item.points = tuple(point_uids[:n])
            self.update_operation(container, items)

            # then
            for item in items:
                retrieved = self.get_operation(container, item.uid)
                self.assertEqual(retrieved, item)
                self.assertNotEqual(item, self.item_list[2])
                self.assertNotEqual(retrieved, self.item_list[2])


class CheckMeshEdgeOperations(CheckMeshElementOperations):

    def setUp(self):
        CheckMeshElementOperations.setUp(self)
        self.addTypeEqualityFunc(
            Edge, partial(compare_elements, testcase=self))

    points_range = [2]

    point_groups = [1, 2]

    @property
    def item_type(self):
        return CUBA.EDGE

    def create_items(self):
        uids = self.uids
        return [Edge(
            points=puids,
            data=create_data_container(restrict=self.supported_cuba()))
            for puids in grouper(uids, 2)]

    def create_item(self, uid):
        uids = self.uids
        return Edge(
            uid=uid,
            points=random.sample(uids, 2),
            data=create_data_container(restrict=self.supported_cuba()))


class CheckMeshFaceOperations(CheckMeshElementOperations):

    def setUp(self):
        CheckMeshElementOperations.setUp(self)
        self.addTypeEqualityFunc(
            Face, partial(compare_elements, testcase=self))

    points_range = [3, 4]

    point_groups = [1, 2, 3, 4]

    @property
    def item_type(self):
        return CUBA.FACE

    def create_items(self):
        uids = self.uids
        return [Face(
            points=puids,
            data=create_data_container(restrict=self.supported_cuba()))
            for puids in grouper(uids, 3)]

    def create_item(self, uid):
        uids = self.uids
        return Face(
            uid=uid,
            points=random.sample(uids, 3),
            data=create_data_container(restrict=self.supported_cuba()))


class CheckMeshCellOperations(CheckMeshElementOperations):

    def setUp(self):
        CheckMeshElementOperations.setUp(self)
        self.addTypeEqualityFunc(
            Cell, partial(compare_elements, testcase=self))

    points_range = range(4, 8)

    point_groups = [1, 2, 3, 4]

    @property
    def item_type(self):
        return CUBA.CELL

    def create_items(self):
        uids = self.uids
        return [Cell(
            points=puids,
            data=create_data_container(restrict=self.supported_cuba()))
            for puids in grouper(uids, 4)]

    def create_item(self, uid):
        uids = self.uids
        return Cell(
            uid=uid,
            points=random.sample(uids, 4),
            data=create_data_container(restrict=self.supported_cuba()))
