"""
This class illustrates use of a particles container class for files
"""
import copy
from simphony.cuds.abc_particle_container import ABCParticleContainer
from simphony.cuds.particle import Particle

import tables


class _ParticleDescription(tables.IsDescription):
    id = tables.Int32Col()
    coordinates = tables.Float64Col(shape=(3,))


class FileParticleContainer(ABCParticleContainer):
    """
    Responsible class to synchronize operations on particles
    """
    def __init__(self, group, file):
        self._group = group
        try:
            self._particles_table = group.particles
        except:
            #create table to hold particles
            self._particles_table = file.create_table(
                group, "particles", _ParticleDescription)

    def add_particle(self, p):
        """Add particle"""
        for r in self._particles_table.where('id == {id}'.format(id=p.id)):
            raise Exception(
                'Particle with id ({id}) already exists'.format(id=p.id))

        #Insert a new particle record
        particle = self._particles_table.row
        particle['id'] = p.id
        particle['coordinates'] = p.coordinates
        particle.append()
        self._particles_table.flush()

    def update_particle(self, p):
        """Update particle"""
        row_indexes = self._particles_table.get_where_list(
            'id == {id}'.format(id=p.id))
        if len(row_indexes) is not 1:
            raise Exception(
                'Particle with id ({id}) does not exist'.format(id=p.id))
        for row in self._particles_table.itersequence(row_indexes):
            row['coordinates'] = list(p.coordinates)
            row.update()
        self._particles_table.flush()

    def get_particle(self, id):
        """Get particle"""
        self._particles_table = self._group.particles

        for r in self._particles_table.where('id == {id}'.format(id=id)):
            p = Particle(r['id'], tuple(r['coordinates']))
            return p

        raise Exception(
            'Particle with id ({id}) does not exist'.format(id=id))

    def remove_particle(self, id):
        """Remove particle"""
        for r in self._particles_table.where('id == {id}'.format(id=id)):
            self._particles_table.remove_rows(r.nrow, r.nrow)
            return
        raise Exception(
            'Particle with id ({id}) does not exist'.format(id=id))

    def iter_particles(self, ids=None):
        """Get iterator over particles"""
        if ids is None:
            ids = []
            for r in self._particles_table:
                ids.append(r['id'])
        else:
            ids = copy.deepcopy(ids)

        while ids:
            particle_id = ids.pop(0)
            yield self.get_particle(particle_id)
