import abc
from functools import partial

import numpy
from numpy.testing import (assert_array_equal, assert_array_almost_equal)

from simphony.testing.utils import (
    create_data_container, compare_data_containers, compare_lattice_nodes)
from simphony.cuds.lattice import (
    LatticeNode, make_cubic_lattice, make_body_centered_cubic_lattice,
    make_face_centered_cubic_lattice, make_rhombohedral_lattice,
    make_hexagonal_lattice, make_tetragonal_lattice,
    make_body_centered_tetragonal_lattice, make_orthorhombic_lattice,
    make_body_centered_orthorhombic_lattice,
    make_face_centered_orthorhombic_lattice,
    make_base_centered_orthorhombic_lattice, make_monoclinic_lattice,
    make_base_centered_monoclinic_lattice, make_triclinic_lattice)
from simphony.core.cuds_item import CUDSItem
from simphony.core.data_container import DataContainer
from simphony.cuds.primitive_cell import (BravaisLattice, PrimitiveCell)


class CheckLatticeContainer(object):

    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self.addTypeEqualityFunc(
            DataContainer, partial(compare_data_containers, testcase=self))
        self.addTypeEqualityFunc(
            LatticeNode, partial(compare_lattice_nodes, testcase=self))
        self.prim_cell = PrimitiveCell.for_cubic_lattice(0.2)
        self.size = (5, 10, 15)
        self.origin = (-2.0, 0.0, 1.0)
        self.container = self.container_factory(
            'my_name', self.prim_cell, self.size, self.origin)

    @abc.abstractmethod
    def container_factory(self, name, prim_cell, size, origin):
        """ Create and return a lattice.
        """

    @abc.abstractmethod
    def supported_cuba(self):
        """ Return a list of CUBA keys to use for restricted containers.
        """

    def test_lattice_properties(self):
        container = self.container

        # check values
        self.assertEqual(container.prim_cell.bravais_lattice,
                         BravaisLattice.CUBIC)
        self.assertEqual(container.name, 'my_name')
        assert_array_equal(container.size, self.size)
        assert_array_equal(container.origin, self.origin)

        # check read-only
        with self.assertRaises(AttributeError):
            container.prim_cell.bravais_lattice = BravaisLattice.CUBIC

        with self.assertRaises(AttributeError):
            container.size = self.size

        with self.assertRaises(AttributeError):
            container.origin = self.origin

        with self.assertRaises(AttributeError):
            container.prim_cell = self.prim_cell

    def test_container_name(self):
        # given/when
        container = self.container

        # then
        self.assertEqual(container.name, 'my_name')

    def test_container_name_update(self):
        # given
        container = self.container

        # when
        container.name = 'new'

        # then
        self.assertEqual(container.name, 'new')

    def test_container_data(self):
        # when
        container = self.container

        # then
        self.assertEqual(container.data, DataContainer())

    def test_container_data_update(self):
        # given
        container = self.container
        data = create_data_container(restrict=self.supported_cuba())

        # when
        container.data = data

        # then
        self.assertEqual(container.data, data)
        self.assertIsNot(container.data, data)

    def test_container_data_update_with_unsupported_cuba(self):
        # given
        container = self.container
        data = create_data_container()
        expected_data = create_data_container(restrict=self.supported_cuba())

        # when
        container.data = data

        # then
        self.assertEqual(container.data, expected_data)
        self.assertIsNot(container.data, expected_data)


class CheckLatticeNodeOperations(object):

    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self.addTypeEqualityFunc(
            DataContainer, partial(compare_data_containers, testcase=self))
        self.addTypeEqualityFunc(
            LatticeNode, partial(compare_lattice_nodes, testcase=self))
        self.prim_cell = PrimitiveCell.for_cubic_lattice(0.2)
        self.size = (5, 10, 15)
        self.origin = (-2.0, 0.0, 1.0)
        self.container = self.container_factory(
            'my_name', self.prim_cell, self.size, self.origin)

    @abc.abstractmethod
    def container_factory(self, name, prim_cell, size, origin):
        """ Create and return a lattice.
        """

    @abc.abstractmethod
    def supported_cuba(self):
        """ Return a list of CUBA keys to use for restricted containers.

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

    def test_update_nodes_with_invalid_index(self):
        container = self.container

        index = 2, 3, 4
        node = container.get_node(index)

        node.index = 2, 300, 4
        with self.assertRaises(IndexError):
            container.update_nodes((node,))

        node.index = 2, 3, -4
        with self.assertRaises(IndexError):
            container.update_nodes((node,))

    def test_update_nodes(self):
        container = self.container

        indices = ((2, 3, 4), (1, 2, 3))
        nodes = [container.get_node(index) for index in indices]
        for node in nodes:
            node.data = create_data_container(restrict=self.supported_cuba())
        container.update_nodes(nodes)

        for n in xrange(len(indices)):
            index = indices[n]
            new_node = container.get_node(index)
            self.assertEqual(new_node, nodes[n])
            # Check that `new_node` is not the same instance as `node`
            self.assertIsNot(new_node, nodes[n])

    def test_update_nodes_with_extra_keywords(self):
        container = self.container

        indices = ((2, 3, 4), (1, 2, 3))
        nodes = [container.get_node(index) for index in indices]
        # Update with full DataContainer.
        for node in nodes:
            node.data = create_data_container()
        container.update_nodes(nodes)

        for n in xrange(len(indices)):
            index = indices[n]
            new_node = container.get_node(index)
            # We expect only the supported CUBA to be stored.
            expected = LatticeNode(
                index=nodes[n].index,
                data=create_data_container(restrict=self.supported_cuba()))
            self.assertEqual(new_node, expected)
            # Check that `new_node` is not the same instance as `node`
            self.assertIsNot(new_node, nodes[n])

    def test_count_of_nodes(self):
        # given
        container = self.container

        # then
        count_original = reduce(lambda x, y: x*y, self.size)
        count_container = container.count_of(CUDSItem.NODE)
        self.assertEqual(count_original, count_container)

    def test_count_of_nodes_passing_unsupported_type(self):
        # given
        container = self.container

        # then
        with self.assertRaises(ValueError):
            container.count_of(CUDSItem.EDGE)


class CheckLatticeNodeCoordinates(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def container_factory(self, name, prim_cell, size, origin):
        """ Create and return a lattice.
        """

    @abc.abstractmethod
    def supported_cuba(self):
        """ Return a list of CUBA keys to use for restricted containers.

        """

    def test_get_coordinate(self):
        """ ABCLattice.get_coordinate is the same for all lattices, therefore
        tested only once.

        """
        default = make_triclinic_lattice(
            'Lattice3', (0.2, 0.4, 0.9), (0.8, 0.4, 0.5), (5, 10, 15),
            (-2.0, 0.0, 1.0))
        container = self.container_factory(
            default.name, default.prim_cell, default.size, default.origin)

        p1 = default.prim_cell.p1
        p2 = default.prim_cell.p2
        p3 = default.prim_cell.p3

        x, y, z = numpy.meshgrid(range(
            default.size[0]), range(default.size[1]), range(default.size[2]))
        indexes = zip(x.flat, y.flat, z.flat)
        expected = zip(
            x.ravel() * p1[0] + y.ravel() * p2[0] + z.ravel() * p3[0] +
                default.origin[0],
            x.ravel() * p1[1] + y.ravel() * p2[1] + z.ravel() * p3[1] +
                default.origin[1],
            x.ravel() * p1[2] + y.ravel() * p2[2] + z.ravel() * p3[2] +
                default.origin[2])

        for i, index in enumerate(indexes):
            assert_array_almost_equal(container.get_coordinate(index),
                                      expected[i])
