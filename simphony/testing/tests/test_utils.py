import unittest
import uuid

import numpy
from numpy.testing import assert_array_equal

from simphony.cuds.particles import Particle, Bond
from simphony.cuds.lattice import LatticeNode
from simphony.cuds.mesh import Point, Element
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from simphony.core.keywords import KEYWORDS
from simphony.testing.utils import (
    compare_particles, create_data_container, compare_bonds,
    compare_lattice_nodes, compare_points, compare_elements,
    create_points, create_bonds, create_particles_with_id,
    compare_data_containers, create_particles,
    create_bonds_with_id, dummy_cuba_value, grouper)


class TestCompareParticles(unittest.TestCase):

    def test_compare_particles_equal(self):
        # given
        particle = Particle(
            uid=None,
            coordinates=(10.0, 0.0, 2.0),
            data=create_data_container())
        reference = Particle(
            uid=None,
            coordinates=(10.0, 0.0, 2.0),
            data=create_data_container())

        # this should pass without problems
        compare_particles(particle, reference, testcase=self)

    def test_compare_particles_not_equal(self):
        # given
        particle = Particle(
            uid=uuid.uuid4(),
            coordinates=(10.0, 0.0, 2.0),
            data=create_data_container())
        reference = Particle(
            uid=uuid.uuid4(),
            coordinates=(10.0, 0.0, 2.0),
            data=create_data_container())

        # when/then
        with self.assertRaises(AssertionError):
            compare_particles(particle, reference, testcase=self)

        # given
        particle = Particle(
            uid=reference.uid,
            coordinates=(340.0, 0.0, 2.0),
            data=create_data_container())

        # when/then
        with self.assertRaises(AssertionError):
            compare_particles(particle, reference, testcase=self)

        # given
        particle = Particle(
            uid=reference.uid,
            coordinates=(10.0, 0.0, 2.0),
            data=DataContainer())

        # when/then
        with self.assertRaises(AssertionError):
            compare_particles(particle, reference, testcase=self)

        # given
        particle = Particle()

        # when/then
        with self.assertRaises(AssertionError):
            compare_particles(particle, reference, testcase=self)


class TestComparePoints(unittest.TestCase):

    def test_compare_points_equal(self):
        # given
        point = Point(
            uid=None,
            coordinates=(10.0, 0.0, 2.0),
            data=create_data_container())
        reference = Point(
            uid=None,
            coordinates=(10.0, 0.0, 2.0),
            data=create_data_container())

        # this should pass without problems
        compare_points(point, reference, testcase=self)

    def test_compare_points_not_equal(self):
        # given
        point = Point(
            uid=uuid.uuid4(),
            coordinates=(10.0, 0.0, 2.0),
            data=create_data_container())
        reference = Point(
            uid=uuid.uuid4(),
            coordinates=(10.0, 0.0, 2.0),
            data=create_data_container())

        # when/then
        with self.assertRaises(AssertionError):
            compare_points(point, reference, testcase=self)

        # given
        point = Point(
            uid=reference.uid,
            coordinates=(10.0, 30.0, 2.0),
            data=create_data_container())

        # when/then
        with self.assertRaises(AssertionError):
            compare_points(point, reference, testcase=self)

        # given
        point = Point(
            uid=reference.uid,
            coordinates=(10.0, 0.0, 2.0),
            data=DataContainer())

        # when/then
        with self.assertRaises(AssertionError):
            compare_points(point, reference, testcase=self)

        # given
        point = Point((0, 0, 0))

        # when/then
        with self.assertRaises(AssertionError):
            compare_points(point, reference, testcase=self)


class TestCompareBonds(unittest.TestCase):

    def test_compare_bonds_equal(self):
        # given
        particles = [uuid.uuid4(), uuid.uuid4()],
        bond = Bond(
            uid=None,
            particles=particles,
            data=create_data_container())
        reference = Bond(
            uid=None,
            particles=particles,
            data=create_data_container())

        # this should pass without problems
        compare_bonds(bond, reference, testcase=self)

    def test_compare_bonds_not_equal(self):
        # given
        particles = [uuid.uuid4(), uuid.uuid4()],
        bond = Bond(
            uid=uuid.uuid4(),
            particles=particles,
            data=create_data_container())
        reference = Bond(
            uid=uuid.uuid4(),
            particles=particles,
            data=create_data_container())

        # when/then
        with self.assertRaises(AssertionError):
            compare_bonds(bond, reference, testcase=self)

        # given
        bond = Bond(
            uid=reference.uid,
            particles=particles[-1],
            data=create_data_container())

        # when/then
        with self.assertRaises(AssertionError):
            compare_bonds(bond, reference, testcase=self)

        # given
        bond = Bond(
            uid=uuid.uuid4(),
            particles=particles,
            data=DataContainer())

        # when/then
        with self.assertRaises(AssertionError):
            compare_bonds(bond, reference, testcase=self)

        # given
        bond = Bond([None])

        # when/then
        with self.assertRaises(AssertionError):
            compare_bonds(bond, reference, testcase=self)


class TestCompareElements(unittest.TestCase):

    def test_compare_elements_equal(self):
        # given
        points = [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()],
        element = Element(
            uid=None,
            points=points,
            data=create_data_container())
        reference = Element(
            uid=None,
            points=points,
            data=create_data_container())

        # this should pass without problems
        compare_elements(element, reference, testcase=self)

        # given
        element = Element(
            uid=None,
            points=list(reversed(points)),
            data=create_data_container())

        # this should pass without problems
        compare_elements(element, reference, testcase=self)

    def test_compare_elements_not_equal(self):
        # given
        points = [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()],
        element = Element(
            uid=uuid.uuid4(),
            points=points,
            data=create_data_container())
        reference = Element(
            uid=uuid.uuid4(),
            points=points,
            data=create_data_container())

        # when/then
        with self.assertRaises(AssertionError):
            compare_elements(element, reference, testcase=self)

        # given
        element = Element(
            uid=reference.uid,
            points=points[1:],
            data=create_data_container())

        # when/then
        with self.assertRaises(AssertionError):
            compare_elements(element, reference, testcase=self)

        # given
        element = Element(
            uid=reference.uid,
            points=points,
            data=DataContainer())

        # when/then
        with self.assertRaises(AssertionError):
            compare_elements(element, reference, testcase=self)

        # given
        element = Element(points=[])

        # when/then
        with self.assertRaises(AssertionError):
            compare_elements(element, reference, testcase=self)


class TestCompareLatticeNodes(unittest.TestCase):

    def test_compare_nodes_equal(self):
        # given
        node = LatticeNode(
            index=(0, 2, 1),
            data=create_data_container())
        reference = LatticeNode(
            index=(0, 2, 1),
            data=create_data_container())

        # this should pass without problems
        compare_lattice_nodes(node, reference, testcase=self)

    def test_compare_nodes_not_equal(self):
        # given
        node = LatticeNode(
            index=(0, 2, 1),
            data=create_data_container())
        reference = LatticeNode(
            index=(1, 2, 1),
            data=create_data_container())

        # when/then
        with self.assertRaises(AssertionError):
            compare_lattice_nodes(node, reference, testcase=self)

        # given
        node = LatticeNode(
            index=(0, 2, 1),
            data=DataContainer())

        # when/then
        with self.assertRaises(AssertionError):
            compare_lattice_nodes(node, reference, testcase=self)

        # given
        node = LatticeNode((0, 0, 0))

        # when/then
        with self.assertRaises(AssertionError):
            compare_lattice_nodes(node, reference, testcase=self)


class TestCompareDataContainers(unittest.TestCase):

    def test_compare_data_containers_equal(self):
        data = create_data_container()
        expected = create_data_container()

        # This should pass without a problem
        compare_data_containers(data, expected, testcase=self)
        compare_data_containers(
            DataContainer(), DataContainer(), testcase=self)
        compare_data_containers({}, DataContainer(), testcase=self)

    def test_compare_data_containers_not_equal(self):
        expected = create_data_container()

        data = create_data_container(constant=1)
        with self.assertRaises(AssertionError):
            compare_data_containers(data, expected, testcase=self)

        data = create_data_container(restrict=[CUBA.MASS])
        with self.assertRaises(AssertionError):
            compare_data_containers(data, expected, testcase=self)


class TestCreateFactories(unittest.TestCase):

    def test_create_points(self):
        points = create_points()
        self.assertEqual(len(points), 6)
        for point in points:
            self.assertIsInstance(point, Point)
            self.assertIsNone(point.uid)
            compare_data_containers(
                point.data, DataContainer(), testcase=self)

    def test_create_particles(self):
        particles = create_particles(n=10)
        self.assertEqual(len(particles), 10)
        for index, particle in enumerate(particles):
            self.assertIsNone(particle.uid)
            self.assertEqual(
                particle.coordinates, (index, index*10, index*100))
            compare_data_containers(
                particle.data, create_data_container(constant=index),
                testcase=self)

    def test_create_particles_with_id(self):
        particles = create_particles_with_id(n=9)
        self.assertEqual(len(particles), 9)
        for index, particle in enumerate(particles):
            self.assertIsInstance(particle, Particle)
            self.assertIsNotNone(particle.uid)
            self.assertEqual(
                particle.coordinates, (index, index*10, index*100))
            compare_data_containers(
                particle.data, create_data_container(),
                testcase=self)

    def test_create_bonds(self):
        n = 7
        bonds = create_bonds(n=n)
        self.assertEqual(len(bonds), n)
        uids = set()
        for index, bond in enumerate(bonds):
            self.assertIsInstance(bond, Bond)
            compare_data_containers(
                bond.data, create_data_container(constant=index),
                testcase=self)
            self.assertEqual(len(bond.particles), n)
            uids.update(bond.particles)
        self.assertEqual(len(uids), n*n)

    def test_create_bonds_with_id(self):
        n = 9
        bonds = create_bonds_with_id(n=n)
        self.assertEqual(len(bonds), n)
        uids = set()
        for index, bond in enumerate(bonds):
            self.assertIsInstance(bond, Bond)
            self.assertIsNotNone(bond.uid)
            compare_data_containers(
                bond.data, create_data_container(),
                testcase=self)
            self.assertEqual(len(bond.particles), n)
            uids.update(bond.particles)
        self.assertEqual(len(uids), n*n)

    def test_create_bonds_with_particles(self):
        n = 7
        particles = create_particles(n=100)
        for particle in particles:
            particle.uid = uuid.uuid4()
        bonds = create_bonds(n=n, particles=particles)
        uids = set()
        self.assertEqual(len(bonds), n)
        for index, bond in enumerate(bonds):
            self.assertIsInstance(bond, Bond)
            compare_data_containers(
                bond.data, create_data_container(constant=index),
                testcase=self)
            self.assertEqual(len(bond.particles), n)
            uids.update(bond.particles)
        self.assertLessEqual(len(uids), n**2)

    def test_create_data_container(self):
        data = create_data_container()
        keys = set(CUBA)
        self.assertEqual(set(data), keys)
        for cuba, value in data.iteritems():
            assert_array_equal(value, dummy_cuba_value(cuba, None))

    def test_create_data_container_with_restrict(self):
        keys = set([CUBA.STATUS, CUBA.MASS])
        data = create_data_container(restrict=keys)
        self.assertEqual(set(data), keys)
        for cuba, value in data.iteritems():
            assert_array_equal(value, dummy_cuba_value(cuba, None))

    def test_create_data_container_with_constant(self):
        data = create_data_container(constant=7)
        keys = set(CUBA)
        self.assertEqual(set(data), keys)
        for cuba, value in data.iteritems():
            assert_array_equal(value, dummy_cuba_value(cuba, 7))

    def test_dummy_cuba_value(self):
        constant = 3
        for cuba in CUBA:
            value = dummy_cuba_value(cuba)
            keyword = KEYWORDS[CUBA(cuba).name]
            if numpy.issubdtype(keyword.dtype, str):
                self.assertEqual(value, keyword.name + str(constant))
            else:
                shape = keyword.shape
                if shape == [1]:
                    self.assertEqual(value, keyword.dtype(cuba + constant))
                else:
                    data = numpy.arange(numpy.prod(shape)) * (cuba + constant)
                    data = numpy.reshape(data, shape)
                    self.assertEqual(value.dtype.type, keyword.dtype)
                    assert_array_equal(value, data)

    def test_dummy_cuba_value_with_constant(self):
        constant = 18
        for cuba in CUBA:
            value = dummy_cuba_value(cuba, constant=18)
            keyword = KEYWORDS[CUBA(cuba).name]
            if numpy.issubdtype(keyword.dtype, str):
                self.assertEqual(value, keyword.name + str(constant))
            else:
                shape = keyword.shape
                if shape == [1]:
                    self.assertEqual(value, keyword.dtype(cuba + constant))
                else:
                    data = numpy.arange(numpy.prod(shape)) * (cuba + constant)
                    data = numpy.reshape(data, shape)
                    self.assertEqual(value.dtype.type, keyword.dtype)
                    assert_array_equal(value, data)


class TestGrouper(unittest.TestCase):

    def test_grouper(self):
        iterable = range(10)

        groups = [group for group in grouper(iterable, 2)]
        self.assertEqual(groups, [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])

    def test_grouper_with_leftover(self):
        iterable = range(10)

        groups = [group for group in grouper(iterable, 3)]
        self.assertEqual(groups, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])

    def test_grouper_with_empty(self):
        iterable = []

        groups = [group for group in grouper(iterable, 3)]
        self.assertEqual(groups, [])
