import abc
import uuid
from functools import partial

from simphony.testing.utils import (
    compare_particles, create_particles, compare_bonds, create_bonds,
    create_data_container)
from simphony.cuds.particles import Particle, Bond
from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer


class ContainerAddParticlesCheck(object):

    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self.addTypeEqualityFunc(
            Particle, partial(compare_particles, testcase=self))
        self.particle_list = create_particles(restrict=self.supported_cuba())
        self.container = self.container_factory('foo')
        self.ids = [
            self.container.add_particle(particle)
            for particle in self.particle_list]

    @abc.abstractmethod
    def container_factory(self, name):
        """ Create and return the container object
        """

    @abc.abstractmethod
    def supported_cuba(self):
        """ Return a list of CUBA keys to use for restricted containers.

        """

    def test_has_particle(self):
        # given and the setUp
        container = self.container

        # then
        self.assertTrue(container.has_particle(self.ids[6]))
        self.assertFalse(container.has_particle(uuid.UUID(int=1234)))

    def test_add_particle(self):
        # given and the setUp
        container = self.container

        # then
        for index, particle in enumerate(self.particle_list):
            self.assertTrue(container.has_particle(particle.uid))
            self.assertEqual(particle.uid, self.ids[index])

    def test_add_particle_with_unsupported_cuba(self):
        # given
        container = self.container
        particle = Particle(
            coordinates=(1, 2, -3),
            data=create_data_container())

        # when
        uid = container.add_particle(particle)

        # then
        particle.data = create_data_container(restrict=self.supported_cuba())
        self.assertTrue(container.has_particle(uid))
        self.assertEqual(container.get_particle(uid), particle)

    def test_add_particle_with_id(self):
        # given
        container = self.container
        uid = uuid.uuid4()
        particle = Particle(
            uid=uid,
            coordinates=(1, 2, -3),
            data=create_data_container(restrict=self.supported_cuba()))

        # when
        particle_uid = container.add_particle(particle)

        # then
        self.assertEqual(particle_uid, uid)
        self.assertTrue(container.has_particle(uid))
        self.assertEqual(container.get_particle(uid), particle)

    def test_exception_when_adding_particle_twice(self):
        # given
        container = self.container

        # then
        with self.assertRaises(ValueError):
            # when
            container.add_particle(self.particle_list[3])


class ContainerManipulatingParticlesCheck(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def container_factory(self, name):
        """ Create and return the container object
        """

    @abc.abstractmethod
    def supported_cuba(self):
        """ Return a list of CUBA keys to use for restricted containers.

        """

    def setUp(self):
        self.addTypeEqualityFunc(
            Particle, partial(compare_particles, testcase=self))
        self.maxDiff = None
        self.particle_list = create_particles(restrict=self.supported_cuba())
        self.particle_list[0].uid = uuid.uuid4()
        self.container = self.container_factory('foo')
        self.ids = [
            self.container.add_particle(particle)
            for particle in self.particle_list]

    def test_get_particle(self):
        # given
        container = self.container

        # when/then
        for uid, particle in map(None, self.ids, self.particle_list):
            self.assertEqual(container.get_particle(uid), particle)

    def test_update_particle(self):
        # given
        container = self.container
        particle = container.get_particle(self.ids[2])
        particle.coordinates = (123, 456, 789)

        # when
        container.update_particle(particle)

        # then
        retrieved = container.get_particle(particle.uid)
        self.assertEqual(retrieved, particle)

    def test_exception_when_update_particle_when_wrong_id(self):
        # given
        container = self.container
        particle = Particle(uid=uuid.uuid4())

        # then
        with self.assertRaises(ValueError):
            # when
            container.update_particle(particle)

        # given
        particle = Particle()

        # then
        with self.assertRaises(ValueError):
            # when
            container.update_particle(particle)

    def test_remove_particle(self):
        # given
        container = self.container
        particle = self.particle_list[1]
        uid = particle.uid

        # when
        container.remove_particle(particle.uid)

        # then
        particles = self.particle_list[:]
        ids = self.ids
        del particles[1]
        del ids[1]
        self.assertFalse(self.container.has_particle(uid))
        for uid, particle in map(None, ids, particles):
            self.assertEqual(container.get_particle(uid), particle)

    def test_exception_when_removing_particle_with_bad_id(self):
        # given
        container = self.container

        # then
        with self.assertRaises(KeyError):
            # when
            container.remove_particle(uuid.UUID(int=23325))

        # then
        with self.assertRaises(KeyError):
            # when
            container.remove_particle(None)

    def test_iter_particles_when_passing_ids(self):
        # given
        particles = [particle for particle in self.particle_list[::2]]
        ids = [particle.uid for particle in particles]

        # when
        iterated_particles = [
            particle for particle in self.container.iter_particles(ids)]

        # then
        for particle, reference in map(None, iterated_particles, particles):
            self.assertEqual(particle, reference)

    def test_iter_all_particles(self):
        # given
        particles = {particle.uid: particle for particle in self.particle_list}

        # when
        iterated_particles = [
            particle for particle in self.container.iter_particles()]

        # then
        # The order of iteration is not important in this case.
        self.assertEqual(len(particles), len(iterated_particles))
        for particle in iterated_particles:
            self.assertEqual(particle, particles[particle.uid])

    def test_exception_on_iter_particles_when_passing_wrong_ids(self):
        # given
        ids = [particle.uid for particle in self.particle_list]
        ids.append(uuid.UUID(int=20))

        # when
        with self.assertRaises(KeyError):
            for particle in self.container.iter_particles(ids):
                pass

        # then
        self.assertEqual(particle.uid, self.particle_list[-1].uid)

    def test_count_of_particles(self):
        # given
        container = self.container
        particle_list = self.particle_list

        # then
        # The order of iteration is not important in this case.
        count_original = len(particle_list)
        count_container = container.count_of(CUBA.PARTICLE)
        self.assertEqual(count_original, count_container)

    def test_count_of_particles_passing_unsupported_type(self):
        # given
        container = self.container

        # then
        # The order of iteration is not important in this case.
        with self.assertRaises(ValueError):
            count_container = container.count_of(CUBA.EDGE)


class ContainerAddBondsCheck(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def container_factory(self, name):
        """ Create and return the container object
        """

    @abc.abstractmethod
    def supported_cuba(self):
        """ Return a list of CUBA keys to use for restricted containers.

        """

    def setUp(self):
        self.addTypeEqualityFunc(
            Bond, partial(compare_bonds, testcase=self))
        self.particle_list = create_particles(restrict=self.supported_cuba())
        self.container = self.container_factory("foo")
        for particle in self.particle_list:
            self.container.add_particle(particle)
        self.bond_list = create_bonds(
            restrict=self.supported_cuba(), particles=self.particle_list)
        self.ids = [
            self.container.add_bond(bond) for bond in self.bond_list]

    def test_has_bond(self):
        # given and setUp
        container = self.container

        # then
        self.assertTrue(container.has_bond(self.ids[2]))
        self.assertFalse(container.has_bond(uuid.UUID(int=2122)))

    def test_add_bond(self):
        # given and setUp
        container = self.container

        # then
        for index, bond in enumerate(self.bond_list):
            self.assertTrue(container.has_bond(bond.uid))
            self.assertEqual(bond.uid, self.ids[index])

    def test_add_bond_with_unsupported_cuba(self):
        # given
        container = self.container
        particles = self.particle_list[0].uid, self.particle_list[-1].uid
        bond = Bond(
            particles=particles,
            data=create_data_container())

        # when
        uid = container.add_bond(bond)

        # then
        bond.data = create_data_container(restrict=self.supported_cuba())
        self.assertTrue(container.has_bond(uid))
        self.assertEqual(container.get_bond(uid), bond)

    def test_add_bond_with_id(self):
        # given
        container = self.container
        uid = uuid.uuid4()
        particles = self.particle_list[0].uid, self.particle_list[-1].uid
        bond = Bond(
            uid=uid,
            particles=particles,
            data=create_data_container(restrict=self.supported_cuba()))

        # when
        bond_uid = container.add_bond(bond)

        # then
        self.assertEqual(bond_uid, uid)
        self.assertTrue(container.has_bond(uid))

    def test_exception_when_adding_bond_twice(self):
        # then
        with self.assertRaises(ValueError):
            # when
            self.container.add_bond(self.bond_list[4])

    def test_exception_when_adding_bond_with_invalid_id(self):
        # then
        with self.assertRaises(ValueError):
            # when
            self.container.add_bond(Bond(uid=object(), particles=[]))


class ContainerManipulatingBondsCheck(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def container_factory(self, name):
        """ Create and return the container object
        """

    @abc.abstractmethod
    def supported_cuba(self):
        """ Return a list of CUBA keys to use for restricted containers.

        """

    def setUp(self):
        self.addTypeEqualityFunc(
            Bond, partial(compare_bonds, testcase=self))
        self.particle_list = create_particles(restrict=self.supported_cuba())
        self.container = self.container_factory("foo")
        for particle in self.particle_list:
            self.container.add_particle(particle)
        self.bond_list = create_bonds(
            restrict=self.supported_cuba(), particles=self.particle_list)
        self.ids = [
            self.container.add_bond(bond) for bond in self.bond_list]

    def test_get_bond(self):
        # given
        container = self.container

        # when/then
        for uid, bond in map(None, self.ids, self.bond_list):
            self.assertEqual(container.get_bond(uid), bond)

    def test_update_bond(self):
        # given
        container = self.container
        bond = container.get_bond(self.ids[1])
        bond.particles = bond.particles[:-1]
        bond.data = DataContainer()

        # when
        container.update_bond(bond)

        # then
        new_bond = container.get_bond(bond.uid)
        self.assertEqual(new_bond, bond)
        self.assertNotEqual(new_bond, self.bond_list[1])

    def test_update_bond_with_unsupported_cuba(self):
        # given
        container = self.container
        bond = container.get_bond(self.ids[1])
        bond.particles = bond.particles[:-1]
        bond.data = create_data_container()

        # when
        container.update_bond(bond)

        # then
        bond.data = create_data_container(restrict=self.supported_cuba())
        new_bond = container.get_bond(bond.uid)
        self.assertEqual(new_bond, bond)
        self.assertNotEqual(new_bond, self.bond_list[1])

    def test_exeception_when_updating_bond_with_incorrect_id(self):
        # given
        bond = Bond([1, 2])

        # then
        with self.assertRaises(ValueError):
            # when
            self.container.update_bond(bond)

    def test_remove_bond(self):
        # given
        container = self.container
        uid = self.ids[1]

        # when
        container.remove_bond(uid)

        # then
        bonds = self.bond_list[:]
        ids = self.ids
        del bonds[1]
        del ids[1]
        self.assertFalse(self.container.has_bond(uid))
        for uid, bond in map(None, ids, bonds):
            self.assertEqual(container.get_bond(uid), bond)

    def test_exception_removing_bond_with_missing_id(self):
        # then
        with self.assertRaises(KeyError):
            # when
            self.container.remove_bond(uuid.UUID(int=12124124))

    def test_iter_bonds_when_passing_ids(self):
        # given
        bonds = [bond for bond in self.bond_list[::2]]
        ids = [bond.uid for bond in bonds]

        # when
        iterated_bonds = [
            bond for bond in self.container.iter_bonds(ids)]

        # then
        for bond, reference in map(None, iterated_bonds, bonds):
            self.assertEqual(bond, reference)

    def test_iter_all_bonds(self):
        # given
        bonds = {bonds.uid: bonds for bonds in self.bond_list}

        # when
        iterated_bonds = [
            bond for bond in self.container.iter_bonds()]

        # then
        # The order of iteration is not important in this case.
        self.assertEqual(len(bonds), len(bonds))
        for bond in iterated_bonds:
            self.assertEqual(bond, bonds[bond.uid])

    def test_exception_on_iter_bonds_when_passing_wrong_ids(self):
        # given
        bonds_ids = self.ids
        bonds_ids.append(uuid.UUID(int=20))

        # when
        with self.assertRaises(KeyError):
            for bond in self.container.iter_bonds(bonds_ids):
                pass

        # then
        self.assertEqual(bond.uid, self.bond_list[-1].uid)

    def test_count_of_bonds(self):
        # given
        container = self.container
        bond_list = self.bond_list

        # then
        # The order of iteration is not important in this case.
        count_original = len(bond_list)
        count_container = container.count_of(CUBA.BOND)
        self.assertEqual(count_original, count_container)

    def test_count_of_bonds_passing_unsupported_type(self):
        # given
        container = self.container

        # then
        # The order of iteration is not important in this case.
        with self.assertRaises(ValueError):
            count_container = container.count_of(CUBA.EDGE)