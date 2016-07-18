import abc
import uuid
from functools import partial

from simphony.testing.utils import (
    compare_particles, create_particles, compare_bonds, create_bonds,
    create_data_container, compare_data_containers,
    create_particles_with_id, create_bonds_with_id)
from simphony.cuds.particles import Particle, Bond
from simphony.core.cuds_item import CUDSItem
from simphony.core.data_container import DataContainer


class CheckParticlesContainer(object):

    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self.addTypeEqualityFunc(
            DataContainer, partial(compare_data_containers, testcase=self))
        self.addTypeEqualityFunc(
            Particle, partial(compare_particles, testcase=self))
        self.container = self.container_factory('my_name')

    @abc.abstractmethod
    def container_factory(self, name):
        """ Create and return a Particles container.
        """

    @abc.abstractmethod
    def supported_cuba(self):
        """ Return a list of CUBA keys to use for restricted containers.
        """

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


class CheckAddingParticles(object):

    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self.addTypeEqualityFunc(
            Particle, partial(compare_particles, testcase=self))
        self.particle_list = create_particles(restrict=self.supported_cuba())
        self.container = self.container_factory('foo')
        self.ids = self.container.add_particles(self.particle_list)

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

    def test_add_particles(self):
        # given and the setUp
        container = self.container

        # then
        for index, particle in enumerate(self.particle_list):
            self.assertTrue(container.has_particle(particle.uid))
            self.assertEqual(particle.uid, self.ids[index])

    def test_add_particles_with_unsupported_cuba(self):
        # given
        container = self.container
        particle = Particle(
            coordinates=(1, 2, -3),
            data=create_data_container())

        # when
        uids = container.add_particles([particle])
        uid = uids[0]

        # then
        particle.data = create_data_container(restrict=self.supported_cuba())
        self.assertTrue(container.has_particle(uid))
        self.assertEqual(container.get_particle(uid), particle)

    def test_add_multiple_particles_with_unsupported_cuba(self):
        # given
        container = self.container
        particles = []
        for i in xrange(10):
            data = create_data_container()
            particles.append(
                Particle([i, i*10, i*100], data=data))

        # when
        container.add_particles(particles)

        # then
        for particle in particles:
            particle.data = create_data_container(
                restrict=self.supported_cuba())
            uid = particle.uid
            self.assertTrue(container.has_particle(uid))
            self.assertEqual(container.get_particle(uid), particle)

    def test_add_particles_with_id(self):
        # given
        container = self.container
        uid = uuid.uuid4()
        particle = Particle(
            uid=uid,
            coordinates=(1, 2, -3),
            data=create_data_container(restrict=self.supported_cuba()))

        # when
        uids = container.add_particles([particle])
        particle_uid = uids[0]

        # then
        self.assertEqual(particle_uid, uid)
        self.assertTrue(container.has_particle(uid))
        self.assertEqual(container.get_particle(uid), particle)

    def test_add_multiple_particles_with_id(self):
        # given
        container = self.container
        particles = create_particles_with_id(restrict=self.supported_cuba())

        # when
        uids = container.add_particles(particles)

        # then
        for particle in particles:
            uid = particle.uid
            self.assertIn(uid, uids)
            self.assertTrue(container.has_particle(uid))
            self.assertEqual(container.get_particle(uid), particle)

    def test_exception_when_adding_particle_twice(self):
        # given
        container = self.container

        # then
        with self.assertRaises(ValueError):
            # when
            container.add_particles([self.particle_list[3]])

    def test_exception_when_adding_multiple_particles_twice(self):
        # given
        container = self.container

        # then
        with self.assertRaises(ValueError):
            # when
            container.add_particles(self.particle_list)


class CheckManipulatingParticles(object):

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
        self.ids = self.container.add_particles(self.particle_list)

    def test_get_particle(self):
        # given
        container = self.container

        # when/then
        for uid, particle in map(None, self.ids, self.particle_list):
            self.assertEqual(container.get_particle(uid), particle)

    def test_update_particles(self):
        # given
        container = self.container
        particle = container.get_particle(self.ids[2])
        particle.coordinates = (123, 456, 789)

        # when
        container.update_particles([particle])

        # then
        retrieved = container.get_particle(particle.uid)
        self.assertEqual(retrieved, particle)

    def test_update_multiple_particles(self):
        # given
        container = self.container
        particles = []
        for uid in self.ids:
            particle = container.get_particle(uid)
            particle.coordinates = (123, 456, 789)
            particles.append(particle)

        # when
        container.update_particles(particles)

        # then
        for uid, particle in map(None, self.ids, particles):
            retrieved = container.get_particle(uid)
            self.assertEqual(retrieved, particle)

    def test_exception_when_update_particles_when_wrong_id(self):
        # given
        container = self.container
        particle = Particle(uid=uuid.uuid4())

        # then
        with self.assertRaises(ValueError):
            # when
            container.update_particles([particle])

        # given
        particle = Particle()

        # then
        with self.assertRaises(ValueError):
            # when
            container.update_particles([particle])

    def test_exception_when_update_multiple_particles_when_wrong_id(self):
        # given
        container = self.container
        particles = create_particles()

        # then
        with self.assertRaises(ValueError):
            # when
            container.update_particles(particles)

        # given
        particles = create_particles_with_id()

        # then
        with self.assertRaises(ValueError):
            # when
            container.update_particles(particles)

    def test_remove_particles(self):
        # given
        container = self.container
        particle = self.particle_list[1]
        uid = particle.uid

        # when
        container.remove_particles([particle.uid])

        # then
        particles = self.particle_list[:]
        ids = self.ids
        del particles[1]
        del ids[1]
        self.assertFalse(self.container.has_particle(uid))
        for uid, particle in map(None, ids, particles):
            self.assertEqual(container.get_particle(uid), particle)

    def test_remove_multiple_particles(self):
        # given
        container = self.container
        uids = [self.particle_list[1].uid, self.particle_list[3].uid]

        # when
        container.remove_particles(uids)

        # then
        particles = self.particle_list[:]
        ids = self.ids
        del particles[3]
        del particles[1]
        del ids[3]
        del ids[1]
        self.assertFalse(self.container.has_particle(uids[0]))
        self.assertFalse(self.container.has_particle(uids[1]))
        for uid, particle in map(None, ids, particles):
            self.assertEqual(container.get_particle(uid), particle)

    def test_exception_when_removing_particle_with_bad_id(self):
        # given
        container = self.container

        # then
        with self.assertRaises(KeyError):
            # when
            container.remove_particles([uuid.UUID(int=23325)])

        # then
        with self.assertRaises(KeyError):
            # when
            container.remove_particles([None])

    def test_exception_when_removing_multiple_particles_with_bad_id(self):
        # given
        container = self.container
        particles = create_particles_with_id()
        uids = [p.uid for p in particles]

        # then
        with self.assertRaises(KeyError):
            # when
            container.remove_particles(uids)

        # then
        with self.assertRaises(KeyError):
            # when
            container.remove_particles([None])

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
        count_original = len(particle_list)
        count_container = container.count_of(CUDSItem.PARTICLE)
        self.assertEqual(count_original, count_container)

    def test_count_of_particles_passing_unsupported_type(self):
        # given
        container = self.container

        # then
        with self.assertRaises(ValueError):
            container.count_of(CUDSItem.EDGE)


class CheckAddingBonds(object):

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
        self.container.add_particles(self.particle_list)
        self.bond_list = create_bonds(
            restrict=self.supported_cuba(), particles=self.particle_list)
        self.ids = self.container.add_bonds(self.bond_list)

    def test_has_bond(self):
        # given and setUp
        container = self.container

        # then
        self.assertTrue(container.has_bond(self.ids[2]))
        self.assertFalse(container.has_bond(uuid.UUID(int=2122)))

    def test_add_bonds(self):
        # given and setUp
        container = self.container

        # then
        for index, bond in enumerate(self.bond_list):
            self.assertTrue(container.has_bond(bond.uid))
            self.assertEqual(bond.uid, self.ids[index])

    def test_add_bonds_with_unsupported_cuba(self):
        # given
        container = self.container
        particles = self.particle_list[0].uid, self.particle_list[-1].uid
        bond = Bond(
            particles=particles,
            data=create_data_container())

        # when
        uids = container.add_bonds([bond])
        uid = uids[0]

        # then
        bond.data = create_data_container(restrict=self.supported_cuba())
        self.assertTrue(container.has_bond(uid))
        self.assertEqual(container.get_bond(uid), bond)

    def test_add_multiple_bonds_with_unsupported_cuba(self):
        # given
        container = self.container
        bonds = []
        for i in xrange(5):
            data = create_data_container()
            ids = [uuid.uuid4() for x in xrange(5)]
            bonds.append(Bond(particles=ids, data=data))

        # when
        container.add_bonds(bonds)

        # then
        for bond in bonds:
            bond.data = create_data_container(
                restrict=self.supported_cuba())
            uid = bond.uid
            self.assertTrue(container.has_bond(uid))
            self.assertEqual(container.get_bond(uid), bond)

    def test_add_bonds_with_id(self):
        # given
        container = self.container
        uid = uuid.uuid4()
        particles = self.particle_list[0].uid, self.particle_list[-1].uid
        bond = Bond(
            uid=uid,
            particles=particles,
            data=create_data_container(restrict=self.supported_cuba()))

        # when
        uids = container.add_bonds([bond])
        bond_uid = uids[0]

        # then
        self.assertEqual(bond_uid, uid)
        self.assertTrue(container.has_bond(uid))

    def test_add_multiple_bonds_with_id(self):
        # given
        container = self.container
        uid = uuid.uuid4()
        bonds = create_bonds_with_id(restrict=self.supported_cuba())

        # when
        uids = container.add_bonds(bonds)

        # then
        for bond in bonds:
            uid = bond.uid
            self.assertIn(uid, uids)
            self.assertTrue(container.has_bond(uid))
            self.assertEqual(container.get_bond(uid), bond)

    def test_exception_when_adding_bond_twice(self):
        # then
        with self.assertRaises(ValueError):
            # when
            self.container.add_bonds([self.bond_list[4]])

    def test_exception_when_adding_multiple_bonds_twice(self):
        # then
        with self.assertRaises(ValueError):
            # when
            self.container.add_bonds(self.bond_list)

    def test_exception_when_adding_bond_with_invalid_id(self):
        # then
        with self.assertRaises(AttributeError):
            # when
            self.container.add_bonds([Bond(uid=object(),
                                     particles=[uuid.uuid4()])])

    def test_exception_when_adding_multiple_bonds_with_invalid_id(self):
        # given
        bonds = [Bond(uid=object(), particles=[uuid.uuid4()]),
                 Bond(uid=object(), particles=[uuid.uuid4()])]
        # then
        with self.assertRaises(AttributeError):
            # when
            self.container.add_bonds(bonds)


class CheckManipulatingBonds(object):

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
        self.container.add_particles(self.particle_list)
        self.bond_list = create_bonds(
            restrict=self.supported_cuba(), particles=self.particle_list)
        self.ids = self.container.add_bonds(self.bond_list)

    def test_get_bond(self):
        # given
        container = self.container

        # when/then
        for uid, bond in map(None, self.ids, self.bond_list):
            self.assertEqual(container.get_bond(uid), bond)

    def test_update_bonds(self):
        # given
        container = self.container
        bond = container.get_bond(self.ids[1])
        bond.particles = bond.particles[:-1]
        bond.data = DataContainer()

        # when
        container.update_bonds([bond])

        # then
        new_bond = container.get_bond(bond.uid)
        self.assertEqual(new_bond, bond)
        self.assertNotEqual(new_bond, self.bond_list[1])

    def test_update_multiple_bonds(self):
        # given
        container = self.container
        bonds = self.bond_list
        uid = uuid.uuid4()
        for bond in bonds:
            bond.particles = (uid,)

        # when
        container.update_bonds(bonds)

        # then
        for uid, bond in map(None, self.ids, bonds):
            retrieved = container.get_bond(uid)
            self.assertEqual(retrieved, bond)

    def test_update_bonds_with_unsupported_cuba(self):
        # given
        container = self.container
        bond = container.get_bond(self.ids[1])
        bond.particles = bond.particles[:-1]
        bond.data = create_data_container()

        # when
        container.update_bonds([bond])

        # then
        bond.data = create_data_container(restrict=self.supported_cuba())
        new_bond = container.get_bond(bond.uid)
        self.assertEqual(new_bond, bond)
        self.assertNotEqual(new_bond, self.bond_list[1])

    def test_update_multiple_bonds_with_unsupported_cuba(self):
        # given
        container = self.container
        updated_bonds = []
        for uid in self.ids:
            bond = container.get_bond(uid)
            bond.particles = bond.particles[:-1]
            bond.data = create_data_container()
            updated_bonds.append(bond)

        # when
        container.update_bonds(updated_bonds)

        # then
        for bond in updated_bonds:
            bond.data = create_data_container(restrict=self.supported_cuba())
        for uid, bond in map(None, self.ids, updated_bonds):
            new_bond = container.get_bond(uid)
            self.assertEqual(new_bond, bond)

    def test_exeception_when_updating_bond_with_incorrect_id(self):
        # given
        bond = Bond([1, 2])

        # then
        with self.assertRaises(ValueError):
            # when
            self.container.update_bonds([bond])

    def test_exeception_when_updating_multiple_bonds_with_incorrect_id(self):
        # given
        bonds = [Bond([1, 2]), Bond([2, 3])]

        # then
        with self.assertRaises(ValueError):
            # when
            self.container.update_bonds(bonds)

    def test_remove_bonds(self):
        # given
        container = self.container
        uid = self.ids[1]

        # when
        container.remove_bonds([uid])

        # then
        bonds = self.bond_list[:]
        ids = self.ids
        del bonds[1]
        del ids[1]
        self.assertFalse(self.container.has_bond(uid))
        for uid, bond in map(None, ids, bonds):
            self.assertEqual(container.get_bond(uid), bond)

    def test_remove_multiple_bonds(self):
        # given
        container = self.container
        uids = [self.ids[1], self.ids[3]]

        # when
        container.remove_bonds(uids)

        # then
        bonds = self.bond_list[:]
        ids = self.ids
        del bonds[3]
        del bonds[1]
        del ids[3]
        del ids[1]
        self.assertFalse(self.container.has_bond(uids[0]))
        self.assertFalse(self.container.has_bond(uids[1]))
        for uid, bond in map(None, ids, bonds):
            self.assertEqual(container.get_bond(uid), bond)

    def test_exception_removing_bond_with_missing_id(self):
        # then
        with self.assertRaises(KeyError):
            # when
            self.container.remove_bonds([uuid.UUID(int=12124124)])

    def test_exception_removing_multiple_bonds_with_missing_id(self):
        # then
        with self.assertRaises(KeyError):
            # when
            self.container.remove_bonds([uuid.UUID(int=12124124),
                                         uuid.UUID(int=19373737)])

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
        count_original = len(bond_list)
        count_container = container.count_of(CUDSItem.BOND)
        self.assertEqual(count_original, count_container)

    def test_count_of_bonds_passing_unsupported_type(self):
        # given
        container = self.container

        # then
        with self.assertRaises(ValueError):
            container.count_of(CUDSItem.EDGE)
