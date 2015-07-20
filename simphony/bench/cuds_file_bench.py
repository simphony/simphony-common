import os
import shutil
import tempfile
import uuid

from simphony.bench.util import bench
from simphony.io.h5_cuds import H5CUDS
from simphony.cuds.particles import Particle, Particles

particles = [
    Particle(coordinates=(0.0, 1.1, 2.2)) for i in range(10000)]

id_particles = [
    Particle(
        uid=uuid.uuid4(),
        coordinates=(0.0, 1.1, 2.2)) for i in range(10000)]


def create_file_with_particles():
    with Container() as pc:
        add_particles_to_container(pc)


def create_file_with_id_particles():
    with Container() as pc:
        add_id_particles_to_container(pc)


def add_id_particles_to_container(particle_container):
    particle_container.add_particles(id_particles)


def add_particles_to_container(particle_container):
    particle_container.add_particles(particles)


def iter_particles_in_container(particle_container):
    return [particle for particle in particle_container.iter_particles()]


def update_coordinates_of_particles_in_container(particle_container):
    updated_particles = []
    for particle in particle_container.iter_particles():
        particle.coordinates = (0.1, 1.0, 1.0)
        updated_particles.append(particle)
    particle_container.update_particles(updated_particles)


class Container(object):
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self._filename = os.path.join(self.temp_dir, 'test.cuds')
        if os.path.exists(self._filename):
            print('exists')

    def __enter__(self):
        self._file = H5CUDS.open(self._filename)
        self._file.add_dataset(Particles("test"))
        return self._file.get_dataset("test")

    def __exit__(self, type, value, tb):
        if os.path.exists(self._filename):
            self._file.close()
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':

    print(
        "create_file_with_particles:",
        bench(lambda: create_file_with_particles(), repeat=3))

    print(
        "create_file_with_id_particles:",
        bench(lambda: create_file_with_id_particles(), repeat=3))

    with Container() as pc:
        add_particles_to_container(pc)
        print(
            "iter_particles_in_container",
            bench(lambda: iter_particles_in_container(pc)))

    with Container() as pc:
        add_particles_to_container(pc)
        print(
            "update_coordinates_of_particles_in_container_using_iter",
            bench(
                lambda: update_coordinates_of_particles_in_container(pc),
                repeat=2))
