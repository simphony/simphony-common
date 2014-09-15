"""
This class illustrates use of a particles container class for files
"""
import copy
import random

import tables
import numpy as np

from simphony.cuds.abc_particle_container import ABCParticleContainer
from simphony.cuds.particle import Particle
from simphony.cuds.bond import Bond


MAX_NUMBER_PARTICLES_IN_BOND = 20


class _ParticleDescription(tables.IsDescription):
    id = tables.Int64Col()
    coordinates = tables.Float64Col(shape=(3,))


class _BondDescription(tables.IsDescription):
    id = tables.Int64Col()
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

    def _create_particles_table(self):
            self._file.create_table(
                self._group, "particles", _ParticleDescription)

    def _create_bonds_table(self):
            self._file.create_table(
                self._group, "bonds", _BondDescription)

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
            for r in self._group.particles.where('id == {id}'.format(id=id)):
                raise ValueError(
                    'Particle (id={id}) already exists'.format(id=id))

        # insert a new particle record
        row = self._group.particles.row
        row['id'] = id
        row['coordinates'] = particle.coordinates
        row.append()
        self._group.particles.flush()
        return id

    def update_particle(self, particle):
        """Update particle"""
        row_indexes = self._group.particles.get_where_list(
            'id == {id}'.format(id=particle.id))
        if len(row_indexes) is not 1:
            raise ValueError(
                'Particle (id={id}) does not exist'.format(id=particle.id))
        for row in self._group.particles.itersequence(row_indexes):
            row['coordinates'] = list(particle.coordinates)
            row.update()
        self._group.particles.flush()

    def get_particle(self, id):
        """Get particle"""
        for r in self._group.particles.where('id == {id}'.format(id=id)):
            return Particle(id=r['id'], coordinates=tuple(r['coordinates']))

        raise ValueError(
            'Particle (id={id}) does not exist'.format(id=id))

    def remove_particle(self, id):
        """Remove particle"""
        index = [r.nrow for r in self._group.particles.where(
            'id == {id}'.format(id=id))]
        if index:
            if self._group.particles.nrows == 1:
                # pytables due to hdf5 limitations does
                # not support removing the last row of table
                # so we delete the table and
                # create new empty table in this situation
                self._group.particles.remove()
                self._create_particles_table()
            else:
                self._group.particles.remove_row(index[0])
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
            ids = copy.deepcopy(ids)
            while ids:
                particle_id = ids.pop(0)
                yield self.get_particle(particle_id)

    def _set_bond_row(self, row, bond, id):
        n = len(bond.particles)
        if n > MAX_NUMBER_PARTICLES_IN_BOND:
            raise Exception(
                'Bond has too many particles ({n} > {maxn})'.format(
                    n=n, maxn=MAX_NUMBER_PARTICLES_IN_BOND))
        row['id'] = id
        row['n_particle_ids'] = n
        particles = list(bond.particles)
        while len(particles) < MAX_NUMBER_PARTICLES_IN_BOND:
            particles.append(0)
        row['particle_ids'] = particles

    def _generate_unique_id(self, table, number_tries=1000):
        max_int = np.iinfo(np.int64).max
        for n in xrange(number_tries):
            id = random.randint(0, max_int)
            for r in table.where('id == {id}'.format(id=id)):
                continue
            return id
        raise Exception('Id could not be generated')

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
            for r in self._group.bonds.where('id == {id}'.format(id=id)):
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
        row_indexes = self._group.bonds.get_where_list(
            'id == {id}'.format(id=bond.id))
        if len(row_indexes) is not 1:
            raise ValueError(
                'Bond (id={id}) does not exist'.format(id=bond.id))
        for row in self._group.bonds.itersequence(row_indexes):
            self._set_bond_row(row, bond, bond.id)
            row.update()
        self._group.bonds.flush()

    def get_bond(self, id):
        """Get bond"""
        for r in self._group.bonds.where('id == {id}'.format(id=id)):
            n = r['n_particle_ids']
            particles = r['particle_ids'][:n]
            return Bond(id=r['id'], particles=tuple(particles))

        raise ValueError(
            'Bond (id={id}) does not exist'.format(id=id))

    def remove_bond(self, id):
        """Remove bond"""
        index = [r.nrow for r in self._group.bonds.where(
            'id == {id}'.format(id=id))]
        if index:
            if self._group.bonds.nrows == 1:
                # pytables due to hdf5 limitations does
                # not support removing the last row of table
                # so we delete the table and
                # create new empty table in this situation
                self._group.bonds.remove()
                self._create_bonds_table()
            else:
                self._group.bonds.remove_row(index[0])
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
            ids = copy.deepcopy(ids)

            while ids:
                bond_id = ids.pop(0)
                yield self.get_bond(bond_id)
