import uuid

import tables
import numpy

from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA

from simphony.cuds.abstractparticles import ABCParticles
from simphony.cuds.particles import Particle, Bond

from simphony.io.h5_cuds_items import H5CUDSItems
from simphony.io.indexed_data_container_table import IndexedDataContainerTable

MAX_NUMBER_PARTICLES_IN_BOND = 20


class _ParticleDescription(tables.IsDescription):
    uid = tables.StringCol(32, pos=0)
    coordinates = tables.Float64Col(pos=1, shape=(3,))


class _BondDescription(tables.IsDescription):
    uid = tables.StringCol(32, pos=0)
    # storing up to fixed number of particles for each bond
    particles = tables.UInt8Col(
        shape=(MAX_NUMBER_PARTICLES_IN_BOND, 16), pos=1)
    n_particles = tables.Int8Col(pos=3)


class H5ParticleItems(H5CUDSItems):
    """ A proxy class to an HDF5 group node with serialised Particles

    The class implements the Mutable-Mapping api where each Particle
    instance is mapped to uid.


    """
    def __init__(self, root, name='particles'):
        """ Create a proxy object for an HDF5 backed particle table.

        Parameters
        ----------
        root : tables.Group
            The root node where to add the particle table structures.
        name : string
            The name of the new group that will be created. Default name is
            'particles'

        """
        super(H5ParticleItems, self).__init__(
            root, name=name, record=_ParticleDescription)

    def _populate(self, row, item):
        """ Populate the row from the Particle.

        """
        self._data[item.uid] = item.data
        row['coordinates'] = list(item.coordinates)

    def _retrieve(self, row):
        """ Return the DataContainer from a table row instance.

        """
        uid = uuid.UUID(hex=row['uid'], version=4)
        return Particle(
            uid=uid, coordinates=row['coordinates'], data=self._data[uid])


class H5BondItems(H5CUDSItems):
    """ A proxy class to an HDF5 group node with serialised Bonds

    The class implements the Mutable-Mapping api where each Bond
    instance is mapped to uid.


    """
    def __init__(self, root, name='bonds'):
        """ Create a proxy object for an HDF5 backed bond table.

        Parameters
        ----------
        root : tables.Group
            The root node where to add the bond table.
        name : string
            The name of the new group that will be created. Default name is
            'bonds'

        """
        super(H5BondItems, self).__init__(
            root, name=name, record=_BondDescription)

    def _populate(self, row, item):
        """ Populate the row from the Particle.

        """
        uid = row['uid']
        self._data[item.uid] = item.data
        particles = item.particles
        number_of_items = len(item.particles)
        row['n_particles'] = number_of_items
        ids = row['particles']
        for index, uid in enumerate(particles):
            ids[index] = numpy.frombuffer(uid.bytes, dtype=numpy.uint8)
        row['particles'] = ids

    def _retrieve(self, row):
        """ Return the DataContainer from a table row instance.

        """
        uid = uuid.UUID(hex=row['uid'], version=4)
        number_of_items = row['n_particles']
        particles = [
            uuid.UUID(bytes=buffer(value), version=4)
            for value in row['particles'][:number_of_items]]
        return Bond(
            uid=uid, particles=particles, data=self._data[uid])


class H5Particles(ABCParticles):
    """ An HDF5 backed particle container.

    """
    def __init__(self, group):
        self._group = group
        self._data = IndexedDataContainerTable(group, 'data')
        self._particles = H5ParticleItems(group, 'particles')
        self._bonds = H5BondItems(group, 'bonds')

        self._items_count = {
            CUBA.PARTICLE: lambda: self._particles,
            CUBA.BOND: lambda: self._bonds
        }

    @property
    def name(self):
        """ The name of the container
        """
        return self._group._v_name

    @name.setter
    def name(self, value):
        self._group._f_rename(value)

    @property
    def data(self):
        if len(self._data) == 1:
            return self._data[0]
        else:
            return DataContainer()

    @data.setter
    def data(self, value):
        if len(self._data) == 0:
            self._data.append(value)
        else:
            self._data[0] = value

    # Particle methods ######################################################

    def add_particle(self, particle):
        """Add particle

        If particle has a uid set then this is used.  If the
        particle's uid is None then a new uid is generated for the
        particle.

        Returns
        -------
        uid : uuid.UUID
            uid of particle.

        Raises
        ------
        ValueError :
           The particle uid already exists in the container.

        """
        uid = particle.uid
        if uid is None:
            uid = uuid.uuid4()
            particle.uid = uid
            self._particles.add_unsafe(particle)
        else:
            self._particles.add_safe(particle)
        return uid

    def update_particle(self, particle):
        self._particles.update_existing(particle)

    def get_particle(self, uid):
        return self._particles[uid]

    def remove_particle(self, uid):
        del self._particles[uid]

    def iter_particles(self, ids=None):
        """Get iterator over particles"""
        if ids is None:
            return iter(self._particles)
        else:
            return self._particles.itersequence(ids)

    def has_particle(self, uid):
        """Checks if a particle with uid "uid" exists in the container."""
        return uid in self._particles

    # Bond methods #######################################################

    def add_bond(self, bond):
        """Add bond

        If bond has an uid then this is used.  If the
        bond's uid is None then a uid is generated for the
        bond.

        Returns
        -------
        uid : uuid.UUID
            uid of bond

        Raises
        ------
        ValueError :
           if an uid is given which already exists.

        """
        uid = bond.uid
        if uid is None:
            uid = uuid.uuid4()
            bond.uid = uid
            self._bonds.add_unsafe(bond)
        else:
            self._bonds.add_safe(bond)
        return uid

    def update_bond(self, bond):
        self._bonds.update_existing(bond)

    def get_bond(self, uid):
        return self._bonds[uid]

    def remove_bond(self, uid):
        del self._bonds[uid]

    def iter_bonds(self, ids=None):
        """Get iterator over particles"""
        if ids is None:
            return iter(self._bonds)
        else:
            return self._bonds.itersequence(ids)

    def has_bond(self, uid):
        """Checks if a bond with uid "uid" exists in the container."""
        return uid in self._bonds

    def count_of(self, item_type):
        """ Return the count of item_type in the container.

        Parameter
        ---------
        item_type : CUBA
            The CUBA enum of the type of the items to return the count of.

        Returns
        -------
        count : int
            The number of items of item_type in the container.

        Raises
        ------
        ValueError :
            If the type of the item is not supported in the current
            container.

        """
        try:
            return len(self._items_count[item_type]())
        except:
            error_str = "Trying to obtain count a of non-supported item: {}"
            raise ValueError(error_str.format(item_type))
