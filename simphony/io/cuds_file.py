""" File access to CUDS-hdf5 formatted files

This module provides access (read/write) to file which are
formated in the CUDS-hdf5 file format
"""

import tables
import copy
from simphony.io.file_particle_container import FileParticleContainer


class CudsFile(object):
    """

    """
    def __init__(self, filename, title=''):
        """

        Parameters
        ----------
        filename : str
            Name of file to be opened. If the file does not exist,
            it will be created.

        title : str
            Title attribute of root node (only applies to new files)
        """

        self._file = tables.open_file(filename, 'a', title=title)
        self._particle_containers = {}

        #create the high-level structure of the cuds file
        for group in ('particle_container', 'lattice', 'mesh'):
            if "/" + group not in self._file:
                self._file.create_group('/', group, group)

    def valid(self):
        """Checks if file is valid (i.e. open)

        """
        if self._file and self._file.isopen:
            return True
        else:
            return False

    @classmethod
    def open(cls, filename, title=''):
        """Opens a file

        """
        return cls(filename, title='')

    def close(self):
        """Closes a file

        """
        self._file.close()

    def add_particle_container(self, name, particle_container):
        """Add particle container to the file.

        Parameters
        ----------
        name : str
            name of particle container
        particle_container
            particle container to be added
        """
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
        """Get particle container from file.

        The returned particle container can be used to query
        and change the related data stored in the file. If the
        file has been closed then the particle container should
        no longer be used.

        Parameters
        ----------
        name : str
            name of particle container to return
        """
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

    def iter_particle_container(self, names=None):
        """Iterate over all or a subset of particle container
        contained in the file.

        Parameters
        ----------
        names : list of str
            names of specific particle containers to be iterated over.
            If names is not given, then all particle containers will
            be iterated over.
        """
        names = copy.deepcopy(names)
        if names is None:
            names = self._particle_containers.keys()
        while names:
            name = names.pop(0)
            yield self.get_particle_container(name)
