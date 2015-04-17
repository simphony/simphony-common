import uuid

import numpy
from numpy.testing import assert_equal

from simphony.core.keywords import KEYWORDS
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from simphony.cuds.particles import Particle, Bond
from simphony.cuds.mesh import Point


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
    self.assertEqual(point.coordinates, point.coordinates)
    compare_data_containers(point.data, point.data, testcase=self)


def compare_elements(element, reference, msg=None, testcase=None):
    self = testcase
    self.assertEqual(element.uid, reference.uid)
    self.assertEqual(element.points, reference.points)
    compare_data_containers(element.data, reference.data, testcase=self)


def compare_lattice_nodes(node, reference, msg=None, testcase=None):
    self = testcase
    self.assertEqual(node.index, reference.index)
    compare_data_containers(node.data, reference.data, testcase=self)


def compare_data_containers(data, reference, msg=None, testcase=None):
    self = testcase
    self.assertEqual(len(data), len(reference))
    for key in data:
        self.assertIn(key, reference)
        self.assertIsInstance(key, CUBA)
        assert_equal(data[key], reference[key])


def create_particles(n=10, restrict=None):
    particle_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict)
        data[CUBA.VELOCITY] = i
        particle_list.append(
            Particle([i, i*10, i*100], data=data))
    return particle_list


def create_points():
    return [
        Point((0.0, 0.0, 0.0)),
        Point((1.0, 0.0, 0.0)),
        Point((0.0, 1.0, 0.0)),
        Point((0.0, 0.0, 1.0)),
        Point((1.0, 0.0, 1.0)),
        Point((0.0, 1.0, 1.0))]


def create_bonds(n=5, restrict=None):
    bond_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict)
        data[CUBA.VELOCITY] = i
        ids = [uuid.uuid4() for x in xrange(n)]
        bond_list.append(Bond(particles=ids, data=data))
    return bond_list


def create_data_container(restrict=None):
    """ Create a dummy data container while respecting the expected data types.

    This is a utility function to be used for testing and prototyping.

    Parameters
    ----------
    restrict : list
        The list of CUBA keys to restrict the value population. Default is to
        use all CUBA keys.

    Returns
    -------
    data : DataContainer


    """

    if restrict is None:
        restrict = CUBA
    data = {cuba: dummy_cuba_value(cuba) for cuba in restrict}
    return DataContainer(data)


def dummy_cuba_value(cuba):
    keyword = KEYWORDS[CUBA(cuba).name]
    # get the data type

    if numpy.issubdtype(keyword.dtype, str):
        return keyword.name
    else:
        shape = keyword.shape
        if shape == [1]:
            if numpy.issubdtype(keyword.dtype, 'float'):
                return float(cuba + 3)
            if numpy.issubdtype(keyword.dtype, 'int'):
                return int(cuba + 3)
        else:
            data = numpy.arange(numpy.prod(shape)) * cuba
            data = numpy.reshape(data, shape)
            if numpy.issubdtype(keyword.dtype, 'float'):
                return numpy.ones(shape=shape, dtype=numpy.float64) * data
            if numpy.issubdtype(keyword.dtype, 'int'):
                return numpy.ones(shape=shape, dtype=numpy.int32) * data

    raise RuntimeError(
        'cannot create value for {}'.format(keyword.dtype))


def grouper(iterable, n):
    """ Collect data into fixed-length chunks or blocks

    """
    iterator = iter(iterable)
    while True:
        yield [next(iterator) for _ in range(n)]
