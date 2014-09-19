"""
This class illustrates use of a particles container class for files
"""
import random

import tables
import numpy

from simphony.cuds.abc_particle_container import ABCParticleContainer
from simphony.cuds.particle import Particle
from simphony.cuds.bond import Bond


MAX_NUMBER_PARTICLES_IN_BOND = 20
MAX_INT = numpy.iinfo(numpy.uint32).max


class _ParticleDescription(tables.IsDescription):
    id = tables.UInt32Col(pos=1)
    coordinates = tables.Float64Col(pos=2, shape=(3,))


class _BondDescription(tables.IsDescription):
    id = tables.UInt32Col()
    # storing up to fixed number of particles for each bond
    particle_ids = tables.Int64Col(shape=(MAX_NUMBER_PARTICLES_IN_BOND,))
    n_particle_ids = tables.Int64Col()


class FileParticleContainer(ABCParticleContainer):
    """
    Responsible class to synchronize operations on particles
    """
    def __init__(self, group, file):
        self._file = file
        self._group = group
        if "particles" not in self._group:
            # create table to hold particles
            self._create_particles_table()

        if "bonds" not in self._group:
            # create table to hold bonds
            self._create_bonds_table()

    # Particle methods ######################################################

    def add_particle(self, particle):
        """Add particle

        If particle has an id then this is used.  If the
        particle's id is None then a id is generated for the
        particle.

        Returns
        -------
        int
            id of particle

        Raises
        -------
        ValueError
           if an id is given which already exists.

        """
        id = particle.id
        if id is None:
            id = self._generate_unique_id(self._group.particles)
        else:
            for _ in self._group.particles.where(
                    'id == value', condvars={'value': id}):
                raise ValueError(
                    'Particle (id={id}) already exists'.format(id=id))

        # insert a new particle record
        self._group.particles.append([(id, particle.coordinates)])
        return id

    def update_particle(self, particle):
        """Update particle"""
        for row in self._group.particles.where(
                'id == value', condvars={'value': particle.id}):
            row['coordinates'] = list(particle.coordinates)
            row.update()
            # see https://github.com/PyTables/PyTables/issues/8
            row._flush_mod_rows()
            return
        else:
            raise ValueError(
                'Particle (id={id}) does not exist'.format(id=particle.id))

    def get_particle(self, id):
        """Get particle"""
        for row in self._group.particles.where(
                'id == value', condvars={'value': id}):
            return Particle(
                id=id, coordinates=tuple(row['coordinates']))
        else:
            raise ValueError(
                'Particle (id={id}) does not exist'.format(id=id))

    def remove_particle(self, id):
        """Remove particle"""
        for row in self._group.particles.where(
                'id == value', condvars={'value': id}):
            if self._group.particles.nrows == 1:
                # pytables due to hdf5 limitations does
                # not support removing the last row of table
                # so we delete the table and
                # create new empty table in this situation
                self._group.particles.remove()
                self._create_particles_table()
            else:
                self._group.particles.remove_row(row.nrow)
            return
        else:
            raise ValueError(
                'Particle (id={id}) does not exist'.format(id=id))

    def iter_particles(self, ids=None):
        """Get iterator over particles"""
        if ids is None:
            for row in self._group.particles:
                yield Particle(
                    id=row['id'], coordinates=tuple(row['coordinates']))
        else:
            # FIXME: we might want to use an indexed query for these cases.
            for particle_id in ids:
                yield self.get_particle(particle_id)

    # Bond methods #######################################################

    def add_bond(self, bond):
        """Add bond

        If bond has an id then this is used.  If the
        bond's id is None then a id is generated for the
        bond.

        Returns
        -------
        int
            id of bond

        Raises
        -------
        ValueError
           if an id is given which already exists.

        """
        id = bond.id
        if id is None:
            id = self._generate_unique_id(self._group.bonds)
        else:
            for r in self._group.bonds.where(
                    'id == value', condvars={'value': id}):
                raise ValueError(
                    'Bond (id={id}) already exists'.format(id=id))

        # insert a new bond record
        row = self._group.bonds.row
        self._set_bond_row(row, bond, id)
        row.append()
        self._group.bonds.flush()
        return id

    def update_bond(self, bond):
        """Update particle"""
        for row in self._group.bonds.where(
                'id == value', condvars={'value': bond.id}):
            self._set_bond_row(row, bond, bond.id)
            row.update()
            # see https://github.com/PyTables/PyTables/issues/8
            row._flush_mod_rows()
            return
        else:
            raise ValueError(
                'Bond (id={id}) does not exist'.format(id=bond.id))

    def get_bond(self, id):
        """Get bond"""
        for row in self._group.bonds.where(
                'id == value', condvars={'value': id}):
            particles = row['particle_ids'][:row['n_particle_ids']]
            # FIXME: do we have to convert to a tuple, why not a list?
            return Bond(id=row['id'], particles=tuple(particles))
        else:
            raise ValueError('Bond (id={id}) does not exist'.format(id=id))

    def remove_bond(self, id):
        """Remove bond"""
        for row in self._group.bonds.where(
                'id == value', condvars={'value': id}):
            if self._group.bonds.nrows == 1:
                # pytables due to hdf5 limitations does
                # not support removing the last row of table
                # so we delete the table and
                # create new empty table in this situation
                self._group.bonds.remove()
                self._create_bonds_table()
            else:
                self._group.bonds.remove_row(row.nrow)
            return
        else:
            raise ValueError(
                'Bond (id={id}) does not exist'.format(id=id))

    def iter_bonds(self, ids=None):
        """Get iterator over bonds"""
        if ids is None:
            for row in self._group.bonds:
                n = row['n_particle_ids']
                particles = row['particle_ids'][:n]
                yield Bond(id=row['id'], particles=tuple(particles))
        else:
            for id in ids:
                yield self.get_bond(id)

    # Private methods #######################################################

    def _create_particles_table(self):
            self._file.create_table(
                self._group, "particles", _ParticleDescription)

    def _create_bonds_table(self):
            self._file.create_table(
                self._group, "bonds", _BondDescription)

    def _set_bond_row(self, row, bond, id):
        n = len(bond.particles)
        if n > MAX_NUMBER_PARTICLES_IN_BOND:
            raise Exception(
                'Bond has too many particles ({n} > {maxn})'.format(
                    n=n, maxn=MAX_NUMBER_PARTICLES_IN_BOND))
        row['id'] = id
        row['n_particle_ids'] = n
        particle_ids = [0] * MAX_NUMBER_PARTICLES_IN_BOND
        particle_ids[:n] = bond.particles
        row['particle_ids'] = particle_ids

    def _generate_unique_id(self, table, number_tries=1000):
        for n in xrange(number_tries):
            id = random.randint(0, MAX_INT)
            for _ in table.where('id == value', condvars={'value': id}):
                break
            else:
                return id
        else:
            raise Exception('Id could not be generated')
