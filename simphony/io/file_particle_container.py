"""
This class illustrates use of a particles container class for files
"""
import copy

import tables

from simphony.cuds.abc_particle_container import ABCParticleContainer
from simphony.cuds.particle import Particle
from simphony.cuds.bond import Bond


MAX_NUMBER_PARTICLES_IN_BOND = 20


class _ParticleDescription(tables.IsDescription):
    id = tables.Int64Col()
    coordinates = tables.Float64Col(shape=(3,))


class _BondDescription(tables.IsDescription):
    id = tables.Int32Col()
    #storing up to fixed number of particles for each bond
    particle_ids = tables.Int64Col(shape=(MAX_NUMBER_PARTICLES_IN_BOND,))
    n_particle_ids = tables.Int64Col()


class FileParticleContainer(ABCParticleContainer):
    """
    Responsible class to synchronize operations on particles
    """
    def __init__(self, group, file):
        self._group = group
        if "particles" not in self._group:
            #create table to hold particles
            file.create_table(group, "particles", _ParticleDescription)

        if "bonds" not in self._group:
            #create table to hold bonds
            file.create_table(group, "bonds", _BondDescription)

    def add_particle(self, p):
        """Add particle"""
        for r in self._group.particles.where('id == {id}'.format(id=p.id)):
            raise Exception(
                'Particle (id={id}) already exists'.format(id=p.id))

        #Insert a new particle record
        particle = self._group.particles.row
        particle['id'] = p.id
        particle['coordinates'] = p.coordinates
        particle.append()
        self._group.particles.flush()

    def update_particle(self, p):
        """Update particle"""
        row_indexes = self._group.particles.get_where_list(
            'id == {id}'.format(id=p.id))
        if len(row_indexes) is not 1:
            raise Exception(
                'Particle (id={id}) does not exist'.format(id=p.id))
        for row in self._group.particles.itersequence(row_indexes):
            row['coordinates'] = list(p.coordinates)
            row.update()
        self._group.particles.flush()

    def get_particle(self, id):
        """Get particle"""
        for r in self._group.particles.where('id == {id}'.format(id=id)):
            return Particle(r['id'], tuple(r['coordinates']))

        raise Exception(
            'Particle (id={id}) does not exist'.format(id=id))

    def remove_particle(self, id):
        """Remove particle"""
        for r in self._group.particles.where('id == {id}'.format(id=id)):
            self._group.particles.remove_rows(r.nrow, r.nrow)
            return
        raise Exception(
            'Particle (id={id}) does not exist'.format(id=id))

    def iter_particles(self, ids=None):
        """Get iterator over particles"""
        if ids is None:
            for row in self._group.particles:
                yield Particle(row['id'], tuple(row['coordinates']))
        else:
            ids = copy.deepcopy(ids)
            while ids:
                particle_id = ids.pop(0)
                yield self.get_particle(particle_id)

    def _set_bond_row(self, row, b):
        n = len(b.particles)
        if n > MAX_NUMBER_PARTICLES_IN_BOND:
            raise Exception(
                'Bond has too many particles ({n} > {maxn})'.format(
                n=n, maxn=MAX_NUMBER_PARTICLES_IN_BOND))
        row['id'] = b.id
        row['n_particle_ids'] = n
        particles = list(b.particles)
        while len(particles) < MAX_NUMBER_PARTICLES_IN_BOND:
            particles.append(0)
        row['particle_ids'] = particles

    def add_bond(self, b):
        """Add bond"""
        for r in self._group.bonds.where('id == {id}'.format(id=b.id)):
            raise Exception(
                'Bond (id={id}) already exists'.format(id=b.id))

        #Insert a new bond record
        row = self._group.bonds.row
        self._set_bond_row(row, b)
        row.append()
        self._group.bonds.flush()

    def update_bond(self, b):
        """Update particle"""
        row_indexes = self._group.bonds.get_where_list(
            'id == {id}'.format(id=b.id))
        if len(row_indexes) is not 1:
            raise Exception(
                'Bond (id={id}) does not exist'.format(id=b.id))
        for row in self._group.bonds.itersequence(row_indexes):
            self._set_bond_row(row, b)
            row.update()
        self._group.bonds.flush()

    def get_bond(self, id):
        """Get bond"""
        for r in self._group.bonds.where('id == {id}'.format(id=id)):
            n = r['n_particle_ids']
            particles = r['particle_ids'][:n]
            return Bond(r['id'], tuple(particles))

        raise Exception(
            'Bond (id={id}) does not exist'.format(id=id))

    def remove_bond(self, id):
        """Remove bond"""
        for r in self._group.bonds.where('id == {id}'.format(id=id)):
            self._group.bonds.remove_rows(r.nrow, r.nrow)
            return
        raise Exception(
            'Bond (id={id}) does not exist'.format(id=id))

    def iter_bonds(self, ids=None):
        """Get iterator over bonds"""
        if ids is None:
            for row in self._group.bonds:
                n = row['n_particle_ids']
                particles = row['particle_ids'][:n]
                yield Bond(row['id'], tuple(particles))
        else:
            ids = copy.deepcopy(ids)

            while ids:
                bond_id = ids.pop(0)
                yield self.get_bond(bond_id)
