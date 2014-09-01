import tables
import copy
from file_particle_container import FileParticleContainer


class CudsFile(object):
    def __init__(self):
        self._file = None
        self._particle_containers = {}

    def open(self, filename, title=''):
        self._file = tables.open_file(filename, 'a', title=title)
        self._particle_containers = {}
        for group in ('particle_container', 'lattice', 'mesh'):
            if "/" + group not in self._file:
                self._file.create_group('/', group, group)

    def close(self):
        self._file.close()
        self._particles_containers = {}

    def add_particle_container(self, name, particle_container):
        if name in self._file.root.particle_container:
            raise Exception(
                'Particle container \'{n}\` already exists'.format(n=name))

        group = self._file.create_group('/particle_container/', name)
        pc = FileParticleContainer(group, self._file)
        self._particle_containers[name] = pc

        for particle in particle_container.iter_particles():
            pc.add_particle(particle)

        self._file.flush()

    def get_particle_container(self, name):
        if name in self._particle_containers:
            return self._particle_containers[name]
        elif name in self._file.root.particle_container:
            group = tables.Group(self._file.root.particle_container, name)
            pc = FileParticleContainer(group, self._file)
            self._particle_containers[name] = pc
            return pc
        else:
            raise Exception(
                'Particle container \'{n}\` does not exist'.format(n=name))

    def iter_particle_container_handles(self, names=None):
        names = copy.deepcopy(names)
        if names is None:
            names = self._particle_containers.keys()
        while names:
            name = names.pop(0)
            yield self.get_particle_container(name)
