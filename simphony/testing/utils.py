import uuid
import random
import collections

import numpy
from numpy.testing import assert_equal

from simphony.core.keywords import KEYWORDS
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from simphony.cuds.particles import Particle, Bond
from simphony.cuds.mesh import Point, Edge, Face, Cell


def compare_particles_datasets(particles, reference, msg=None, testcase=None):
    self = testcase
    self.assertEqual(particles.name, reference.name)
    for b, r in zip(particles.iter_bonds(), reference.iter_bonds()):
        compare_bonds(b, r, testcase=self)
    for p, r in zip(particles.iter_particles(), reference.iter_particles()):
        compare_particles(p, r, testcase=self)
    compare_data_containers(particles.data, reference.data, testcase=self)


def compare_mesh_datasets(mesh, reference, msg=None, testcase=None):
    self = testcase
    self.assertEqual(mesh.name, reference.name)
    for p, r in zip(mesh.iter_points(), reference.iter_points()):
        compare_points(p, r, testcase=self)
    for e, r in zip(mesh.iter_edges(), reference.iter_edges()):
        compare_elements(e, r, testcase=self)
    for f, r in zip(mesh.iter_faces(), reference.iter_faces()):
        compare_elements(f, r, testcase=self)
    for c, r in zip(mesh.iter_cells(), reference.iter_cells()):
        compare_elements(c, r, testcase=self)
    compare_data_containers(mesh.data, reference.data, testcase=self)


def compare_lattice_datasets(lattice, reference, msg=None, testcase=None):
    self = testcase
    self.assertEqual(lattice.name, reference.name)
    for l, r in zip(lattice.iter_nodes(), reference.iter_nodes()):
        compare_lattice_nodes(l, r, testcase=self)
    compare_data_containers(lattice.data, reference.data, testcase=self)
    self.assertEqual(lattice.type, reference.type)
    numpy.testing.assert_array_equal(lattice.base_vect, reference.base_vect)
    self.assertEqual(lattice.size, reference.size)
    numpy.testing.assert_array_equal(lattice.origin, reference.origin)


def compare_bonds(bond, reference, msg=None, testcase=None):
    self = testcase
    self.assertEqual(bond.uid, reference.uid)
    self.assertEqual(bond.particles, reference.particles)
    compare_data_containers(bond.data, reference.data, testcase=self)


def compare_particles(particle, reference, msg=None, testcase=None):
    self = testcase
    self.assertEqual(particle.uid, reference.uid)
    self.assertEqual(particle.coordinates, reference.coordinates)
    compare_data_containers(particle.data, reference.data, testcase=self)


def compare_points(point, reference, msg=None, testcase=None):
    self = testcase
    self.assertEqual(point.uid, reference.uid)
    self.assertEqual(point.coordinates, reference.coordinates)
    compare_data_containers(point.data, reference.data, testcase=self)


def compare_elements(element, reference, msg=None, testcase=None):
    self = testcase
    self.assertEqual(element.uid, reference.uid)
    points = collections.deque(reference.points)
    for _ in range(len(points)):
        points.rotate(1)
        try:
            self.assertSequenceEqual(element.points, points)
        except AssertionError:
            continue
        else:
            break
    else:
        message = 'Point uid sequences are not equivalent: {} !~ {}'
        raise AssertionError(message.format(element.points, reference.points))

    compare_data_containers(element.data, reference.data, testcase=self)


def compare_lattice_nodes(node, reference, msg=None, testcase=None):
    self = testcase
    self.assertEqual(node.index, reference.index)
    compare_data_containers(node.data, reference.data, testcase=self)


def compare_data_containers(data, reference, msg=None, testcase=None):
    self = testcase
    self.assertEqual(set(data), set(reference))
    for key in data:
        self.assertIn(key, reference)
        self.assertIsInstance(key, CUBA)
        message = "Values for {} are not equal\n ACTUAL: {}\n DESIRED: {}"
        assert_equal(
            data[key], reference[key],
            err_msg=message.format(key.name, data[key], reference[key]),
            verbose=False)


def create_particles(n=10, restrict=None):
    particle_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict, constant=i)
        particle_list.append(
            Particle([i, i*10, i*100], data=data))
    return particle_list


def create_particles_with_id(n=10, restrict=None):
    particle_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict, constant=i)
        uid = uuid.uuid4()
        particle_list.append(
            Particle(uid=uid,
                     coordinates=[i, i*10, i*100],
                     data=data))
    return particle_list


def create_points(n=10, restrict=None):
    point_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict, constant=i)
        point_list.append(
            Point(uid=None,
                  coordinates=[i, i*10, i*100],
                  data=data))
    return point_list


def create_points_with_id(n=10, restrict=None):
    point_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict, constant=i)
        uid = uuid.uuid4()
        point_list.append(
            Point(uid=uid,
                  coordinates=[i, i*10, i*100],
                  data=data))
    return point_list


def create_bonds(n=5, restrict=None, particles=None):
    bond_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict, constant=i)
        if particles is None:
            ids = [uuid.uuid4() for x in xrange(n)]
        else:
            uids = [particle.uid for particle in particles]
            ids = random.sample(uids, n)
        bond_list.append(Bond(particles=ids, data=data))
    return bond_list


def create_bonds_with_id(n=5, restrict=None, particles=None):
    bond_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict)
        uid = uuid.uuid4()
        if particles is None:
            ids = [uuid.uuid4() for x in xrange(n)]
        else:
            uids = [particle.uid for particle in particles]
            ids = random.sample(uids, n)
        bond_list.append(Bond(uid=uid, particles=ids, data=data))
    return bond_list


def create_edges(n=5, restrict=None, points=None):
    edge_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict, constant=i)
        if points is None:
            ids = [uuid.uuid4() for x in xrange(2)]
        else:
            uids = [point.uid for point in points]
            ids = random.sample(uids, 2)
        edge_list.append(
            Edge(uid=None,
                 points=ids,
                 data=data))
    return edge_list


def create_edges_with_id(n=5, restrict=None, points=None):
    edge_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict, constant=i)
        uid = uuid.uuid4()
        if points is None:
            ids = [uuid.uuid4() for x in xrange(2)]
        else:
            uids = [point.uid for point in points]
            ids = random.sample(uids, 2)
        edge_list.append(
            Edge(uid=uid,
                 points=ids,
                 data=data))
    return edge_list


def create_faces(n=5, restrict=None, points=None):
    face_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict, constant=i)
        if points is None:
            ids = [uuid.uuid4() for x in xrange(3)]
        else:
            uids = [point.uid for point in points]
            ids = random.sample(uids, 3)
        face_list.append(
            Face(uid=None,
                 points=ids,
                 data=data))
    return face_list


def create_faces_with_id(n=5, restrict=None, points=None):
    face_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict, constant=i)
        uid = uuid.uuid4()
        if points is None:
            ids = [uuid.uuid4() for x in xrange(3)]
        else:
            uids = [point.uid for point in points]
            ids = random.sample(uids, 3)
        face_list.append(
            Face(uid=uid,
                 points=ids,
                 data=data))
    return face_list


def create_cells(n=5, restrict=None, points=None):
    cell_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict, constant=i)
        if points is None:
            ids = [uuid.uuid4() for x in xrange(4)]
        else:
            uids = [point.uid for point in points]
            ids = random.sample(uids, 4)
        cell_list.append(
            Cell(uid=None,
                 points=ids,
                 data=data))
    return cell_list


def create_cells_with_id(n=5, restrict=None, points=None):
    cell_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict, constant=i)
        uid = uuid.uuid4()
        if points is None:
            ids = [uuid.uuid4() for x in xrange(4)]
        else:
            uids = [point.uid for point in points]
            ids = random.sample(uids, 4)
        cell_list.append(
            Cell(uid=uid,
                 points=ids,
                 data=data))
    return cell_list


def create_data_container(restrict=None, constant=None):
    """ Create a dummy data container while respecting the expected data types.

    This is a utility function to be used for testing and prototyping.

    Parameters
    ----------
    restrict : list
        The list of CUBA keys to restrict the value population. Default is to
        use all CUBA keys.

    constant : int
        A numerical constant to create the dummy value. Default is None.

    Returns
    -------
    data : DataContainer

    """
    if restrict is None:
        restrict = CUBA
    data = {cuba: dummy_cuba_value(cuba, constant) for cuba in restrict}
    return DataContainer(data)


def dummy_cuba_value(cuba, constant=None):
    """ Create a dummy value for the CUBA keyword.

    Parameters
    ----------
    cuba : CUBA
        The cuba key to get a dummy value back

    constant : int
        A numerical constant to create the dummy value. Default is 3.

    Returns
    -------
    value :
        A dummy value following the dtype description of the CUBA keyword.

    """
    if constant is None:
        constant = 3
    keyword = KEYWORDS[CUBA(cuba).name]
    if numpy.issubdtype(keyword.dtype, str):
        return keyword.name + str(constant)
    else:
        shape = keyword.shape
        if shape == [1]:
            if numpy.issubdtype(keyword.dtype, 'float'):
                return float(cuba + constant)
            if numpy.issubdtype(keyword.dtype, 'int'):
                return int(cuba + constant)
        else:
            data = numpy.arange(numpy.prod(shape)) * (cuba + constant)
            data = numpy.reshape(data, shape)
            if numpy.issubdtype(keyword.dtype, 'float'):
                return numpy.ones(shape=shape, dtype=numpy.float64) * data
            if numpy.issubdtype(keyword.dtype, 'int'):
                return numpy.ones(shape=shape, dtype=numpy.int32) * data

    raise RuntimeError(
        'cannot create value for {}'.format(keyword.dtype))


def grouper(iterable, n):
    """ Collect data into fixed-length chunks or blocks

    .. note::

       If the iterable is exhausted before a valid chuck is collected
       then the last chuck is ignored and the iteration ends.

    """
    iterator = iter(iterable)
    while True:
        yield [next(iterator) for _ in range(n)]
