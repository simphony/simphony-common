""" File access to CUDS-hdf5 formatted files

This module provides access (read/write) to file which are
formated in the CUDS-hdf5 file format
"""

import copy

import tables

from simphony.io.file_particle_container import FileParticleContainer


class CudsFile(object):
    """ Access to CUDS-hdf5 formatted files

    """
    def __init__(self, file):
        """

        Parameters
        ----------
        file : table.file
            file to be used

        """

        if not isinstance(file, tables.File):
            raise ValueError(
                "File should be a Pytable file")

        if file.mode is 'r':
            raise ValueError(
                "File should not be opened in read-only mode")

        self._file = file
        self._particle_containers = {}
        self._mesh_containers = {}

    def valid(self):
        """Checks if file is valid (i.e. open)

        """
        return self._file is not None and self._file.isopen

    @classmethod
    def open(cls, filename, mode="a", title=''):
        """Returns a SimPhony file and returns an opened CudsFile

        Parameters
        ----------
        filename : str
            Name of file to be opened.


        mode: str
            The mode to open the file:
                * *'w'*: Write; a new file is created (an existing file
                  with the same name would be deleted).
                * *'a'*: Append; an existing file is opened for reading and
                  writing, and if the file does not exist it is created.


        title : str
            Title attribute of root node (only applies to a file which
              is being created

        """
        if mode not in ('a', 'w'):
            raise ValueError(
                "Invalid mode string ''%s''. Only "
                "'a' and 'w' are acceptable modes " % mode)

        file = tables.open_file(filename, mode, title=title)

        # create the high-level structure of the cuds file
        for group in ('particle_container', 'lattice', 'mesh'):
            if "/" + group not in file:
                file.create_group('/', group, group)

        return cls(file)

    def close(self):
        """Closes a file

        """
        self._file.close()

    def add_particle_container(self, name, particle_container=None):
        """Add particle container to the file.

        Parameters
        ----------
        name : str
            name of particle container
        particle_container : ABCParticleContainer, optional
            particle container to be added. If none is give,
            then an empty particle container is added.

        Returns
        ----------
        FileParticleContainer
            The particle container newly added to the file.  See
            get_particle_container for more information.

        """
        if name in self._file.root.particle_container:
            raise ValueError(
                'Particle container \'{n}\` already exists'.format(n=name))

        group = self._file.create_group('/particle_container/', name)
        pc = FileParticleContainer(group, self._file)
        self._particle_containers[name] = (pc, group)

        if particle_container:
            # copy the contents of the particle container to the file
            for particle in particle_container.iter_particles():
                pc.add_particle(particle)
            for bond in particle_container.iter_bonds():
                pc.add_bond(bond)

        self._file.flush()
        return pc

    def add_mesh_container(self, name, mesh_container=None):
        """Add particle container to the file.

        Parameters
        ----------
        name : str
            name of the mesh container
        mesh_container : ABCMeshContainer, optional
            mesh container to be added. If none is give,
            then an empty mesh container is added.

        Returns
        ----------
        FileMeshContainer
            The mesh container newly added to the file.  
            See get_mesh_container for more information.

        """
        if name in self._file.root.mesh_container:
            raise ValueError(
                'Mesh container \'{n}\` already exists'.format(n=name))

        group = self._file.create_group('/mesh_container/', name)
        mc = FileMeshContainer(group, self._file)
        self._mesh_containers[name] = (mc, group)

        if mesh_container:
            # copy the contents of the mesh container to the file
            for point in mesh_container.iter_points():
                pc.add_point(point)
            for edge in mesh_container.iter_edges():
                pc.add_edge(bond)
            for face in mesh_container.iter_faces():
                pc.add_face(bond)
            for cell in mesh_container.iter_cells():
                pc.add_cell(bond)

        self._file.flush()
        return pc

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
            return self._particle_containers[name][0]
        elif name in self._file.root.particle_container:
            group = tables.Group(self._file.root.particle_container, name)
            pc = FileParticleContainer(group, self._file)
            self._particle_containers[name] = pc
            return pc
        else:
            raise ValueError(
                'Particle container \'{n}\` does not exist'.format(n=name))

    def get_mesh_container(self, name):
        """Get mesh container from file.

        The returned mesh container can be used to query
        and change the related data stored in the file. If the
        file has been closed then the mesh container should
        no longer be used.

        Parameters
        ----------
        name : str
            name of the mesh container to return
        """

        if name in self._mesh_containers:
            return self._mesh_containers[name][0]
        elif name in self._file.root.mesh_container:
            group = tables.Group(self._file.root.mesh_container, name)
            mc = FileMeshContainer(group, self._file)
            self._mesh_containers[name] = pc
            return mc
        else:
            raise ValueError(
                'Mesh container \'{n}\` does not exist'.format(n=name))


    def delete_particle_container(self, name):
        """Delete particle container from file.

        Parameters
        ----------
        name : str
            name of particle container to delete
        """
        if name in self._particle_containers:
            self._particle_containers[name][1]._f_remove(recursive=True)
            del self._particle_containers[name]
        else:
            raise ValueError(
                'Particle container \'{n}\` does not exist'.format(n=name))

    def delete_mesh_container(self, name):
        """Delete mesh container from file.

        Parameters
        ----------
        name : str
            name of the mesh container to delete
        """

        if name in self._mesh_containers:
            self._mesh_containers[name][1]._f_remove(recursive=True)
            del self._mesh_containers[name]
        else:
            raise ValueError(
                'Mesh container \'{n}\` does not exist'.format(n=name))


    def iter_particle_containers(self, names=None):
        """Returns an iterator over a subset or all
        of the particle containers. The iterator iterator yields
        (name, particlecontainer) tuples for each particle container
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
        for name in names:
            yield self.get_particle_container(name), name

    def iter_mesh_containers(self, names=None):
        """Returns an iterator over a subset or all
        of the mesh containers. The iterator iterator yields
        (name, meshcontainer) tuples for each mesh container
        contained in the file.

        Parameters
        ----------
        names : list of str
            names of specific mesh containers to be iterated over.
            If names is not given, then all mesh containers will
            be iterated over.

        """

        names = copy.deepcopy(names)
        if names is None:
            names = self._mesh_containers.keys()
        for name in names:
            yield self.get_mesh_container(name), name
