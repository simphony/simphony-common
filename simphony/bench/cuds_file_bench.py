from __future__ import print_function

import os
import shutil
import tempfile

from simphony.bench.util import bench
from simphony.io.cuds_file import CudsFile
from simphony.cuds.particle import Particle

particles = [
    Particle(coordinates=(0.0, 1.1, 2.2)) for i in range(10000)]

id_particles = [
    Particle(id=i, coordinates=(0.0, 1.1, 2.2)) for i in range(10000)]


def create_file_with_particles():
    with Container() as pc:
        add_particles_to_container(pc)


def create_file_with_id_particles():
    with Container() as pc:
        add_id_particles_to_container(pc)


def add_id_particles_to_container(particle_container):
    for particle in id_particles:
        particle_container.add_particle(particle)


def add_particles_to_container(particle_container):
    for particle in particles:
        particle_container.add_particle(particle)


def iter_particles_in_container(particle_container):
    return [particle for particle in particle_container.iter_particles()]


def update_coordinates_of_particles_in_container(particle_container):
    for particle in particle_container.iter_particles():
        particle.coordinates = (0.1, 1.0, 1.0)
        particle_container.update_particle(particle)


class Container(object):
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self._filename = os.path.join(self.temp_dir, 'test.cuds')
        if os.path.exists(self._filename):
            print('exists')

    def __enter__(self):
        self._file = CudsFile.open(self._filename)
        pc = self._file.add_particle_container("test")
        return pc

    def __exit__(self, type, value, tb):
        if os.path.exists(self._filename):
            self._file.close()
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':

    print(
        "create_file_with_particles:",
        bench(lambda: create_file_with_particles(), repeat=2))

    print(
        "create_file_with_particles:",
        bench(lambda: create_file_with_id_particles(), repeat=2))

    with Container() as pc:
        add_particles_to_container(pc)
        print(
            "iter_particles_in_file",
            bench(lambda: iter_particles_in_container(pc)))

    with Container() as pc:
        add_particles_to_container(pc)
        print(
            "update_coordinates_of_particles_in_file_using_iter",
            bench(
                lambda: update_coordinates_of_particles_in_container(pc),
                repeat=2))
