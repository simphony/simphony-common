import abc
from functools import partial

import numpy
from numpy.testing import assert_array_equal

from simphony.testing.utils import (
    create_data_container, compare_data_containers, compare_lattice_nodes)
from simphony.cuds.lattice import LatticeNode
from simphony.core.data_container import DataContainer


class ABCCheckLattice(object):

    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self.addTypeEqualityFunc(
            DataContainer, partial(compare_data_containers, testcase=self))
        self.addTypeEqualityFunc(
            LatticeNode, partial(compare_lattice_nodes, testcase=self))
        self.size = (5, 10, 15)
        self.base_vect = (0.1, 0.2, 0.3)
        self.origin = (-2.0, 0.0, 1.0)
        self.container = self.container_factory(
            'foo', 'Cubic', self.base_vect, self.size, self.origin)

    @abc.abstractmethod
    def container_factory(self, name, type_, base_vect, size, origin):
        """ Create and return a lattice.
        """

    def test_iter_nodes(self):
        container = self.container

        # number of nodes
        number_of_nodes = sum(1 for node in container.iter_nodes())
        self.assertEqual(number_of_nodes, numpy.prod(self.size))

        # data
        for node in container.iter_nodes():
            self.assertEqual(node.data, DataContainer())

        # indexes
        x, y, z = numpy.meshgrid(
            range(self.size[0]), range(self.size[1]), range(self.size[2]))
        expected = set(zip(x.flat, y.flat, z.flat))
        indexes = {node.index for node in container.iter_nodes()}
        self.assertEqual(indexes, expected)

    def test_iter_nodes_subset(self):
        container = self.container

        x, y, z = numpy.meshgrid(
            range(2, self.size[0]),
            range(self.size[1]-4),
            range(3, self.size[2], 2))
        expected = set(zip(x.flat, y.flat, z.flat))

        # data
        for node in container.iter_nodes(expected):
            self.assertEqual(node.data, DataContainer())

        # indexes
        indexes = {node.index for node in container.iter_nodes(expected)}
        self.assertEqual(indexes, expected)

    def test_get_node(self):
        container = self.container

        index = 2, 3, 4
        node = container.get_node(index)
        expected = LatticeNode(index)
        self.assertEqual(node, expected)

        # check that mutating the node does not change internal info
        node.data = create_data_container()
        self.assertNotEqual(container.get_node(index), node)

    def test_get_node_with_invalid_index(self):
        container = self.container

        index = 2, 300, 4
        with self.assertRaises(IndexError):
            container.get_node(index)

        index = 2, 3, -4
        with self.assertRaises(IndexError):
            container.get_node(index)

    def test_update_node(self):
        container = self.container

        index = 2, 3, 4
        node = container.get_node(index)
        node.data = create_data_container()
        container.update_node(node)

        new_node = container.get_node(index)
        self.assertEqual(new_node, node)
        # Check that `new_node` is not the same instance as `node`
        self.assertIsNot(new_node, node)

    def test_get_coordinate(self):
        container = self.container

        xspace, yspace, zspace = self.base_vect
        x, y, z = numpy.meshgrid(
            range(self.size[0]), range(self.size[1]), range(self.size[2]))
        indexes = zip(x.flat, y.flat, z.flat)
        expected = zip(
            x.ravel() * xspace + self.origin[0],
            y.ravel() * yspace + self.origin[1],
            z.ravel() * zspace + self.origin[2])

        for i, index in enumerate(indexes):
            assert_array_equal(container.get_coordinate(index), expected[i])

    def test_lattive_properties(self):
        container = self.container

        # check values
        self.assertEqual(container.type, 'Cubic')
        self.assertEqual(container.name, 'foo')
        assert_array_equal(container.size, self.size)
        assert_array_equal(container.origin, self.origin)
        assert_array_equal(container.base_vect, self.base_vect)

        # check read-only
        with self.assertRaises(AttributeError):
            container.type = 'Cubic'

        with self.assertRaises(AttributeError):
            container.size = self.size

        with self.assertRaises(AttributeError):
            container.origin = self.origin

        with self.assertRaises(AttributeError):
            container.base_vect = self.base_vect

        # check read-write
        container.name = 'boo'
        self.assertEqual(container.name, 'boo')
