from __future__ import print_function

import os

from simphony.bench.util import bench
from simphony.io.cuds_file import CudsFile
from simphony.cuds.particle import Particle


def create_file_with_particles():
    file = CudsFile.open('test.cuds')
    pc = file.add_particle_container("test")
    for i in xrange(10000):
        pc.add_particle(Particle(id=i, coordinates=(0.0, 1.1, 2.2)))
    file.close()
    os.remove('test.cuds')


def iter_particles_in_file(particle_container):
    id = 0
    for p in particle_container.iter_particles():
        id = p.id
    return id


def update_coordinates_of_particles_in_file_using_iter(particle_container):
    for p in particle_container.iter_particles():
        p.coordinates = (0.1, 1.0, 1.0)
        particle_container.update_particle(p)


class FilledParticleContainer(object):
    def __init__(self):
        pass

    def __enter__(self):
        self._file = CudsFile.open('test.cuds')
        pc = self._file.add_particle_container("test")
        for i in xrange(10000):
            pc.add_particle(Particle(id=i, coordinates=(0.0, 1.1, 2.2)))
        return pc

    def __exit__(self, type, value, tb):
        self._file.close()
        os.remove('test.cuds')


if __name__ == '__main__':
    print("create_file_with_particles:", bench(
        lambda: create_file_with_particles()))

    with FilledParticleContainer() as pc:
        print("iter_particles_in_file", bench(
            lambda: iter_particles_in_file(pc)))

        print("update_coordinates_of_particles_in_file_using_iter", bench(
            lambda: update_coordinates_of_particles_in_file_using_iter(pc)))
