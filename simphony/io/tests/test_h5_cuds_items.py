import tempfile
import shutil
import os
import random
import uuid
import unittest
from contextlib import closing, contextmanager
from collections import OrderedDict

import tables
from numpy.testing import assert_equal

from simphony.io.h5_cuds_items import H5CUDSItems
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from simphony.testing.utils import (
    create_data_container, dummy_cuba_value, compare_data_containers)


class _DummyRecord(tables.IsDescription):
    uid = tables.StringCol(32, pos=0)
    value = tables.IntCol(pos=1)


class _DummyItem(object):

    def __init__(self, uid=None, value=None, data=None):
        self.uid = uid
        self.data = DataContainer() if data is None else DataContainer(data)
        self.value = -1 if value is None else value


class _DummyH5CUDSItems(H5CUDSItems):

    def _populate(self, row, item):
        row['value'] = item.value
        self._data[item.uid] = item.data

    def _retrieve(self, row):
        uid = uuid.UUID(hex=row['uid'], version=4)
        return _DummyItem(uid=uid, value=row['value'], data=self._data[uid])


class TestH5CUDSItems(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(_DummyItem, self.compare_dummy_items)
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')
        self.maxDiff = None

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    @contextmanager
    def new_container(self, name):
        handle = None
        try:
            handle = tables.open_file(self.filename, mode='w')
            root = handle.root
            container = _DummyH5CUDSItems(root, name=name, record=_DummyRecord)
            self.assertEqual(len(container), 0)
            yield container
        finally:
            if handle is not None:
                handle.close()

    @contextmanager
    def open_container(self, name, mode='r'):
        handle = None
        try:
            handle = tables.open_file(self.filename, mode=mode)
            root = handle.root
            container = _DummyH5CUDSItems(
                root, name=name, record=_DummyRecord)
            yield container
        finally:
            if handle is not None:
                handle.close()

    @property
    def item_list(self):
        item_list = []
        for i in xrange(10):
            data = create_data_container()
            data[CUBA.VELOCITY] = i
            item_list.append(_DummyItem(data=data, value=i))
        return item_list

    def compare_dummy_items(self, item, reference, msg=None):
        self.assertEqual(item.uid, reference.uid)
        self.assertEqual(item.value, reference.value)
        compare_data_containers(item.data, reference.data, testcase=self)

    def test_creating_a_item_container(self):
        with closing(tables.open_file(self.filename, mode='w')) as handle:
            root = handle.root
            container = _DummyH5CUDSItems(
                root, name='my_items', record=_DummyRecord)
            self.assertEqual(len(container), 0)
            self.assertIn('my_items', root)
            self.assertIn('items', root.my_items)
            self.assertIn('data', root.my_items)
            self.assertTrue(container.valid)

    def test_add_unsafe(self):
        item_list = self.item_list
        for item in item_list[:-1]:
            item.uid = uuid.uuid4()
        item_list[-1].uid = item_list[0].uid  # duplicate uid
        with self.new_container('my_items') as container:
            for item in item_list:
                container.add_unsafe(item)
        with self.open_container('my_items') as container:
            with self.assertRaises(RuntimeError):
                self.assertEqual(len(container), 10)
            for item in item_list[1:-1]:
                self.assertEqual(container[item.uid], item)
            with self.assertRaises(AssertionError):
                # one of the following assertions should fail
                item = item_list[-1]
                self.assertEqual(container[item.uid], item)
                item = item_list[0]
                self.assertEqual(container[item.uid], item)

    def test_add_safe(self):
        item_list = self.item_list
        for item in item_list[:-1]:
            item.uid = uuid.uuid4()
        item_list[-1].uid = item_list[0].uid  # duplicate uid
        with self.new_container('my_items') as container:
            for item in item_list[:-1]:
                container.add_safe(item)
            with self.assertRaises(ValueError):
                container.add_safe(item_list[-1])
        with self.open_container('my_items') as container:
            self.assertEqual(len(container), 9)
            for item in item_list[:-1]:
                self.assertEqual(container[item.uid], item)

    def test_setitem(self):
        with self.new_container('my_items') as container:
            uids = {uuid.uuid4(): item for item in self.item_list}
            for uid, item in uids.iteritems():
                container[uid] = item
        with self.open_container('my_items') as container:
            self.assertEqual(len(container), 10)
            for uid, item in uids.iteritems():
                self.assertEqual(container[uid], item)

    def test_getitem(self):
        with self.new_container('my_items') as container:
            uids = {uuid.uuid4(): item for item in self.item_list}
            for uid, item in uids.iteritems():
                container[uid] = item
        with self.open_container('my_items') as container:
            self.assertEqual(len(container), 10)
            for uid in uids:
                self.assertEqual(container[uid], uids[uid])

    def test_getitem_with_invalid_uid(self):
        with self.new_container('my_items') as container:
            uids = {uuid.uuid4(): item for item in self.item_list}
            for uid, item in uids.iteritems():
                container[uid] = item
        with self.open_container('my_items') as table:
            with self.assertRaises(KeyError):
                table[uuid.uuid4()]

    def test_update_data(self):
        item_list = self.item_list
        with self.new_container('my_items') as container:
            uids = OrderedDict()
            for item in item_list:
                uid = uuid.uuid4()
                item.uid = uid
                uids[uid] = item
                container[uid] = item
        with self.open_container('my_items', mode='a') as container:
            updated_items = [item for item in reversed(item_list)]
            for uid in uids:
                for item in updated_items:
                    item.uid = uid
                    container[uid] = item
                    self.assertEqual(container[uid], item)

    def test_delete_data(self):
        with self.new_container('my_items') as container:
            uids = {uuid.uuid4(): item for item in self.item_list}
            for uid, item in uids.iteritems():
                container[uid] = item
        with self.open_container('my_items', mode='a') as container:
            del container[uids.keys()[0]]
            for uid in uids.keys()[1:]:
                self.assertEqual(container[uid], uids[uid])

    def test_delete_data_with_invalid_uid(self):
        with self.new_container('my_items') as container:
            uids = {uuid.uuid4(): item for item in self.item_list}
            for uid, item in uids.iteritems():
                container[uid] = item
        with self.open_container('my_items', mode='a') as container:
            uid = uids.keys()[0]
            del container[uid]
            with self.assertRaises(KeyError):
                del container[uuid.uuid4()]
            with self.assertRaises(KeyError):
                del container[uid]

    def test_delete_data_to_empty_table(self):
        uid = uuid.uuid4()
        item = self.item_list[0]
        item.uid = uid

        with closing(tables.open_file(self.filename, mode='a')) as handle:
            root = handle.root
            container = _DummyH5CUDSItems(
                root, name='my_items', record=_DummyRecord)
            container[uid] = item
            self.assertEqual(len(container), 1)
            del container[uid]
            self.assertEqual(len(container), 0)
            self.assertIn('my_items', root)
            self.assertIn('items', root.my_items)
            self.assertIn('data', root.my_items)
            self.assertTrue(container.valid)

    def test_iteration(self):
        # add to data container table
        with self.new_container('my_items') as container:
            uids = {uuid.uuid4(): item for item in self.item_list}
            for uid, item in uids.iteritems():
                container[uid] = item
            self.assertEqual(len(container), len(uids))

        # Iterate over all the rows
        with self.open_container('my_items', mode='a') as container:
            for index, loaded_data in enumerate(container):
                self.assertEqual(loaded_data, uids[loaded_data.uid])
            self.assertEqual(index,  len(uids) - 1)

    def test_itersequence(self):
        with self.new_container('my_items') as container:
            uids = {uuid.uuid4(): item for item in self.item_list}
            for uid, item in uids.iteritems():
                container[uid] = item
            self.assertEqual(len(container), len(uids))

        # Iterate over a sequence of rows
        with self.open_container('my_items') as container:
            sequence = random.sample(uids, 4)
            loaded_data = [
                item for item in container.itersequence(sequence)]
            self.assertEqual(len(loaded_data), 4)
            for index, item in enumerate(loaded_data):
                self.assertEqual(item, uids[sequence[index]])


if __name__ == '__main__':
    unittest.main()
