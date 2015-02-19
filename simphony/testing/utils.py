import uuid

import numpy
from numpy.testing import assert_equal

from simphony.io.data_container_description import Data
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from simphony.cuds.particles import Particle, Bond


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


def compare_data_containers(data, reference, msg=None, testcase=None):
    self = testcase
    self.assertEqual(len(data), len(reference))
    for key in data:
        self.assertIn(key, reference)
        assert_equal(data[key], reference[key])


def create_particles(n=10, restrict=None):
    particle_list = []
    for i in xrange(n):
        data = create_data_container(restrict=restrict)
        data[CUBA.VELOCITY] = i
        particle_list.append(
            Particle([i, i*10, i*100], data=data))
    return particle_list


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
    column = CUBA(cuba).name.lower()
    # get the column type
    try:
        column_type = Data.columns[column]
    except AttributeError:
        column_type = Data._v_colobjects[column]

    if numpy.issubdtype(column_type, str):
        value = column.upper()
    elif numpy.issubdtype(column_type, numpy.float):
        value = float(cuba + 3)
    elif numpy.issubdtype(column_type, numpy.integer):
        value = int(cuba + 3)
    else:
        shape = column_type.shape
        data = numpy.arange(numpy.prod(shape)) * cuba
        data = numpy.reshape(data, shape)
        if column_type.kind == 'float':
            value = numpy.ones(
                shape=shape, dtype=numpy.float64) * data
        elif column_type.kind == 'int':
            value = numpy.ones(
                shape=shape, dtype=numpy.int32) * data
        else:
            raise RuntimeError(
                'cannot create value for {}'.format(column_type))
    return value
