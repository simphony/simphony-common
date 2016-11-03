from __future__ import print_function

import random
import tempfile
import os.path
import shutil
from contextlib import closing

import tables

from .util import bench
from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer
from simphony.io.indexed_data_container_table import (
    IndexedDataContainerTable)
from simphony.testing.utils import create_data_container


temp_dir = tempfile.mkdtemp()
filename = os.path.join(temp_dir, 'sample_file.cuds')
n = 1000

dict_data = create_data_container()
dict_data_half = create_data_container()
for i, cuba in enumerate(CUBA):
    if i % 2:
        continue
    del dict_data_half[cuba]

data_container = DataContainer(dict_data)
data_container_half = DataContainer(dict_data_half)


def append(handle, n, value):
    root = handle.root
    if hasattr(root, 'my_data_table'):
        handle.remove_node(root, 'my_data_table', recursive=True)
    table = IndexedDataContainerTable(root, 'my_data_table', expected_number=n)
    return [table.append(value) for i in range(n)]


def set_item(handle, uids, value):
    root = handle.root
    if hasattr(root, 'my_data_table'):
        handle.remove_node(root, 'my_data_table', recursive=True)
    table = IndexedDataContainerTable(root, 'my_data_table', expected_number=n)
    for uid in uids:
        table[uid] = value


def iteration(container):
    for i in container:
        pass


def iteration_with_sequence(container, indices):
    for i in container.itersequence(indices):
        pass


def getitem_access(table, indices):
    return [table[index] for index in indices]


def setitem(table, value, indices):
    for index in indices:
        table[index] = value


def delitem(table, indices):
    for index in indices:
        del table[index]


def create_table(filename):
    with closing(tables.open_file(filename, mode='w')) as handle:
        uids = append(handle, 1000, data_container)
    return uids


def main():
    try:
        print("""
        Benchmarking various operations on the IndexDataContainerTable.

        """)
        with closing(tables.open_file(filename, mode='w')) as handle:
            root = handle.root
            table = IndexedDataContainerTable(root, 'my_data_table')
            print(
                "Append {}:".format(n),
                bench(lambda: append(handle, 1000, data_container)))

        with closing(tables.open_file(filename, mode='w')) as handle:
            root = handle.root
            table = IndexedDataContainerTable(
                root, 'my_data_table', expected_number=n)
            print(
                "Append {} masked:".format(n),
                bench(lambda: append(handle, 1000, data_container_half)))

        uids = create_table(filename)
        sample = random.sample(uids, 300)

        with closing(tables.open_file(filename, mode='r')) as handle:
            root = handle.root
            table = IndexedDataContainerTable(
                root, 'my_data_table', expected_number=n)
            print("Iterate {}:".format(n), bench(lambda: iteration(table)))
            print(
                'Getitem sample of 300:',
                bench(lambda: getitem_access(table, sample)))

        with closing(tables.open_file(filename, mode='a')) as handle:
            root = handle.root
            table = IndexedDataContainerTable(
                root, 'my_data_table', expected_number=n)
            print(
                "Update item of 300 sample:",
                bench(lambda: setitem(table, data_container_half, sample)))
    finally:
        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    main()
