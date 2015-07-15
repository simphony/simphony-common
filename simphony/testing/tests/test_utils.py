import abc
import unittest
import uuid

import numpy
from numpy.testing import assert_array_equal

from simphony.cuds.particles import Particles, Particle, Bond
from simphony.cuds.lattice import Lattice, LatticeNode
from simphony.cuds.mesh import Mesh, Point, Element, Edge, Face, Cell
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from simphony.core.keywords import KEYWORDS
from simphony.testing.utils import (
    compare_particles, create_data_container, compare_bonds,
    compare_lattice_nodes, compare_points, compare_elements,
    create_points, create_bonds, create_bonds_with_id,
    compare_data_containers, create_particles, dummy_cuba_value, 
    grouper, compare_particles_datasets, compare_mesh_datasets,
    compare_lattice_datasets, create_particles_with_id,
    create_points_with_id, create_edges, create_faces,
    create_cells, create_edges_with_id, create_faces_with_id,
    create_cells_with_id)


class TestCompareParticlesDatasets(unittest.TestCase):

    def test_compare_particles_datasets_equal(self):
        # given
        particles = Particles(name="test")
        reference = Particles(name="test")

        particle_list = create_particles_with_id()
        bond_list = create_bonds()
        data = DataContainer()

        particles.add_particles(particle_list)
        reference.add_particles(particle_list)

        particles.add_bonds(bond_list)
        reference.add_bonds(bond_list)

        particles.data = data
        reference.data = data

        # this should pass without problems
        compare_particles_datasets(particles, reference, testcase=self)

    def test_compare_particles_datasets_not_equal(self):
        # given
        particles = Particles(name="test")
        reference = Particles(name="test_ref")

        particle_list = create_particles_with_id()
        bond_list = create_bonds()
        data = create_data_container()

        particles.add_particles(particle_list)
        reference.add_particles(particle_list)

        particles.add_bonds(bond_list)
        reference.add_bonds(bond_list)

        particles.data = data
        reference.data = data

        # when/then
        with self.assertRaises(AssertionError):
            compare_particles_datasets(particles, reference, testcase=self)

        # given
        test_particles = create_particles_with_id()

        particles = Particles(name=reference.name)
        particles.add_particles(test_particles)
        particles.add_bonds(bond_list)
        particles.data = data

        # when/then
        with self.assertRaises(AssertionError):
            compare_particles_datasets(particles, reference, testcase=self)

        # given
        test_bonds = create_bonds()

        particles = Particles(name=reference.name)
        particles.add_particles(particle_list)
        particles.add_bonds(test_bonds)
        particles.data = data

        # when/then
        with self.assertRaises(AssertionError):
            compare_particles_datasets(particles, reference, testcase=self)

        # given
        test_data = DataContainer()

        particles = Particles(name=reference.name)
        particles.add_particles(particle_list)
        particles.add_bonds(bond_list)
        particles.data = test_data

        # when/then
        with self.assertRaises(AssertionError):
            compare_particles_datasets(particles, reference, testcase=self)


class TestCompareMeshDatasets(unittest.TestCase):

    def test_compare_mesh_datasets_equal(self):
        # given
        mesh = Mesh(name="test")
        reference = Mesh(name="test")

        point_list = create_particles_with_id()
        edge_list = create_edges()
        face_list = create_faces()
        cell_list = create_cells()

        data = DataContainer()

        for point in point_list:
            mesh.add_point(point)
            reference.add_point(point)
        for edge in edge_list:
            mesh.add_edge(edge)
            reference.add_edge(edge)
        for face in face_list:
            mesh.add_face(face)
            reference.add_face(face)
        for cell in cell_list:
            mesh.add_cell(cell)
            reference.add_cell(cell)

        mesh.data = data
        reference.data = data

        # this should pass without problems
        compare_mesh_datasets(mesh, reference, testcase=self)

    def test_compare_mesh_datasets_not_equal(self):
        # given
        mesh = Mesh(name="test")
        reference = Mesh(name="test_ref")

        point_list = create_particles_with_id()
        edge_list = create_edges()
        face_list = create_faces()
        cell_list = create_cells()

        data = create_data_container()

        for point in point_list:
            mesh.add_point(point)
            reference.add_point(point)
        for edge in edge_list:
            mesh.add_edge(edge)
            reference.add_edge(edge)
        for face in face_list:
            mesh.add_face(face)
            reference.add_face(face)
        for cell in cell_list:
            mesh.add_cell(cell)
            reference.add_cell(cell)

        mesh.data = data
        reference.data = data

        # when/then
        with self.assertRaises(AssertionError):
            compare_mesh_datasets(mesh, reference, testcase=self)

        # given
        test_points = create_points_with_id()

        mesh = Mesh(name=reference.name)
        for point in test_points:
            mesh.add_point(point)
        for edge in edge_list:
            mesh.add_edge(edge)
        for face in face_list:
            mesh.add_face(face)
        for cell in cell_list:
            mesh.add_cell(cell)
        mesh.data = data

        # when/then
        with self.assertRaises(AssertionError):
            compare_mesh_datasets(mesh, reference, testcase=self)

        # given
        test_edges = create_edges()

        mesh = Mesh(name=reference.name)
        for point in point_list:
            mesh.add_point(point)
        for edge in test_edges:
            mesh.add_edge(edge)
        for face in face_list:
            mesh.add_face(face)
        for cell in cell_list:
            mesh.add_cell(cell)
        mesh.data = data

        # when/then
        with self.assertRaises(AssertionError):
            compare_mesh_datasets(mesh, reference, testcase=self)

        # given
        test_faces = create_faces()

        mesh = Mesh(name=reference.name)
        for point in point_list:
            mesh.add_point(point)
        for edge in edge_list:
            mesh.add_edge(edge)
        for face in test_faces:
            mesh.add_face(face)
        for cell in cell_list:
            mesh.add_cell(cell)
        mesh.data = data

        # when/then
        with self.assertRaises(AssertionError):
            compare_mesh_datasets(mesh, reference, testcase=self)

        # given
        test_cells = create_cells()

        mesh = Mesh(name=reference.name)
        for point in point_list:
            mesh.add_point(point)
        for edge in edge_list:
            mesh.add_edge(edge)
        for face in face_list:
            mesh.add_face(face)
        for cell in test_cells:
            mesh.add_cell(cell)
        mesh.data = data

        # when/then
        with self.assertRaises(AssertionError):
            compare_mesh_datasets(mesh, reference, testcase=self)

        # given
        test_data = DataContainer()

        mesh = Mesh(name=reference.name)
        for point in point_list:
            mesh.add_point(point)
        for edge in edge_list:
            mesh.add_edge(edge)
        for face in face_list:
            mesh.add_face(face)
        for cell in cell_list:
            mesh.add_cell(cell)
        mesh.data = test_data

        # when/then
        with self.assertRaises(AssertionError):
            compare_mesh_datasets(mesh, reference, testcase=self)


class TestCompareLatticeDatasets(unittest.TestCase):

    def test_compare_lattice_datasets_equal(self):
        # given
        lattice = Lattice(
            'test', 'cubic', (1.0, 1.0, 1.0),
            (2, 3, 4), (0.0, 0.0, 0.0))
        reference = Lattice(
            'test', 'cubic', (1.0, 1.0, 1.0),
            (2, 3, 4), (0.0, 0.0, 0.0))

        data = DataContainer()

        lattice.data = data
        reference.data = data

        # this should pass without problems
        compare_lattice_datasets(lattice, reference, testcase=self)

    def test_compare_lattice_datasets_not_equal(self):
        # given
        lattice = Lattice(
            'test', 'cubic', (1.0, 1.0, 1.0),
            (2, 3, 4), (0.0, 0.0, 0.0))
        reference = Lattice(
            'test_ref', 'cubic', (1.0, 1.0, 1.0),
            (2, 3, 4), (0.0, 0.0, 0.0))

        data = create_data_container()

        lattice.data = data
        reference.data = data

        # when/then
        with self.assertRaises(AssertionError):
            compare_lattice_datasets(lattice, reference, testcase=self)

        # given
        test_data = DataContainer()

        lattice = Lattice(
            'test_ref', 'cubic', (1.0, 1.0, 1.0),
            (2, 3, 4), (0.0, 0.0, 0.0))
        lattice.data = test_data

        # when/then
        with self.assertRaises(AssertionError):
            compare_lattice_datasets(lattice, reference, testcase=self)

        # given
        lattice = Lattice(
            'test_ref', 'cubic', (2.0, 2.0, 2.0),
            (2, 3, 4), (0.0, 0.0, 0.0))
        lattice.data = data

        # when/then
        with self.assertRaises(AssertionError):
            compare_lattice_datasets(lattice, reference, testcase=self)

        # given
        lattice = Lattice(
            'test_ref', 'cubic', (1.0, 1.0, 1.0),
            (4, 6, 8), (0.0, 0.0, 0.0))
        lattice.data = data

        # when/then
        with self.assertRaises(AssertionError):
            compare_lattice_datasets(lattice, reference, testcase=self)

        # given
        lattice = Lattice(
            'test_ref', 'cubic', (1.0, 1.0, 1.0),
            (2, 3, 4), (2.0, 2.0, 2.0))
        lattice.data = data

        # when/then
        with self.assertRaises(AssertionError):
            compare_lattice_datasets(lattice, reference, testcase=self)


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


class CreateElementsFactory(object):

    __metaclass__ = abc.ABCMeta

    classtype = None
    itemsPerContainer = 0

    @abc.abstractmethod
    def container_factory(self, n, items):
        """ Create and return the container object
        """

    @abc.abstractmethod
    def item_factory(self, n):
        """ Create and return the container object
        """

    def test_create_factory(self):
        n_containers = 7
        n_items = self.itemsPerContainer
        containers = self.container_factory(n=n_containers, items=None)
        self.assertEqual(len(containers), n_containers)
        uids = set()
        for index, container in enumerate(containers):
            self.assertIsInstance(container, self.classtype)
            compare_data_containers(
                container.data, create_data_container(constant=index),
                testcase=self)
            self.assertEqual(len(container.points), n_items)
            uids.update(container.points)
        self.assertLessEqual(len(uids), n_containers*n_items)

    def test_create_factory_with_points(self):
        n_containers = 7
        n_items = self.itemsPerContainer
        items = self.item_factory(n=10)
        containers = self.container_factory(n=n_containers, items=items)
        uids = set()
        self.assertEqual(len(containers), n_containers)
        for index, container in enumerate(containers):
            self.assertIsInstance(container, self.classtype)
            compare_data_containers(
                container.data, create_data_container(constant=index),
                testcase=self)
            self.assertEqual(len(container.points), n_items)
            uids.update(container.points)
        self.assertLessEqual(len(uids), n_containers*n_items)


class TestCreateEdgesFactory(CreateElementsFactory, unittest.TestCase):

    classtype = Edge
    itemsPerContainer = 2

    def container_factory(self, n, items):
        """ Create and return the container object
        """
        return create_edges(n=n, points=items)

    def item_factory(self, n):
        """ Create and return the container object
        """
        return create_points(n=n)


class TestCreateEdgesFactoryWithId(CreateElementsFactory, unittest.TestCase):

    classtype = Edge
    itemsPerContainer = 2

    def container_factory(self, n, items):
        """ Create and return the container object
        """
        return create_edges_with_id(n=n, points=items)

    def item_factory(self, n):
        """ Create and return the container object
        """
        return create_points_with_id(n=n)


class TestCreateFacesFactory(CreateElementsFactory, unittest.TestCase):

    classtype = Face
    itemsPerContainer = 3

    def container_factory(self, n, items):
        """ Create and return the container object
        """
        return create_faces(n=n, points=items)

    def item_factory(self, n):
        """ Create and return the container object
        """
        return create_points(n=n)


class TestCreateFacesFactoryWithId(CreateElementsFactory, unittest.TestCase):

    classtype = Face
    itemsPerContainer = 3

    def container_factory(self, n, items):
        """ Create and return the container object
        """
        return create_faces_with_id(n=n, points=items)

    def item_factory(self, n):
        """ Create and return the container object
        """
        return create_points_with_id(n=n)


class TestCreateCellsFactory(CreateElementsFactory, unittest.TestCase):

    classtype = Cell
    itemsPerContainer = 4

    def container_factory(self, n, items):
        """ Create and return the container object
        """
        return create_cells(n=n, points=items)

    def item_factory(self, n):
        """ Create and return the container object
        """
        return create_points(n=n)


class TestCreateCellsFactoryWithId(CreateElementsFactory, unittest.TestCase):

    classtype = Cell
    itemsPerContainer = 4

    def container_factory(self, n, items):
        """ Create and return the container object
        """
        return create_cells_with_id(n=n, points=items)

    def item_factory(self, n):
        """ Create and return the container object
        """
        return create_points_with_id(n=n)


class TestCreateFactories(unittest.TestCase):

    def test_create_points(self):
        points = create_points(n=10)
        self.assertEqual(len(points), 10)
        for index, point in enumerate(points):
            self.assertIsInstance(point, Point)
            self.assertIsNone(point.uid)
            self.assertEqual(
                point.coordinates, (index, index*10, index*100))
            compare_data_containers(
                point.data, create_data_container(constant=index),
                testcase=self)

    def test_create_points_with_id(self):
        points = create_points_with_id(n=10)
        self.assertEqual(len(points), 10)
        for index, point in enumerate(points):
            self.assertIsInstance(point, Point)
            self.assertIsNotNone(point.uid)
            self.assertEqual(
                point.coordinates, (index, index*10, index*100))
            compare_data_containers(
                point.data, create_data_container(),
                testcase=self)

    def test_create_particles(self):
        particles = create_particles(n=10)
        self.assertEqual(len(particles), 10)
        for index, particle in enumerate(particles):
            self.assertIsInstance(particle, Particle)
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


if __name__ == '__main__':
    unittest.main()
