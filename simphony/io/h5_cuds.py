import copy

import tables

from simphony.io.file_particle_container import FileParticleContainer
from simphony.io.file_mesh import FileMesh


class H5CUDS(object):
    """ Access to CUDS-hdf5 formatted files.

    """

    def __init__(self, file):
        """ Create/Open a CUDS file.

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

    def valid(self):
        """Checks if file is valid (i.e. open)

        """
        return self._file is not None and self._file.isopen

    @classmethod
    def open(cls, filename, mode="a", title=''):
        """ Returns a SimPhony file and returns an opened CudsFile

        Parameters
        ----------
        filename : str
            Name of file to be opened.

        mode: str
            The mode to open the file:

            - ``w`` -- Write; a new file is created (an existing file
              with the same name would be deleted).
            - ``a`` -- Append; an existing file is opened for reading and
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

    def add_particle_container(self, particle_container):
        """Add particle container to the file.

        Parameters
        ----------
        particle_container : ABCParticleContainer
            particle container to be added.

        Returns
        -------
        FileParticleContainer
            The particle container newly added to the file.  See
            get_particle_container for more information.

        """
        if particle_container.name in self._file.root.particle_container:
            raise ValueError(
                'Particle container \'{n}\` already exists'.format(
                    n=particle_container.name))

        group = self._file.create_group(
            '/particle_container/', particle_container.name)
        pc = FileParticleContainer(group, self._file)

        if particle_container:
            # copy the contents of the particle container to the file
            for particle in particle_container.iter_particles():
                pc.add_particle(particle)
            for bond in particle_container.iter_bonds():
                pc.add_bond(bond)

        self._file.flush()
        return pc

    def add_mesh(self, mesh):
        """Add a mesh to the file.

        Parameters
        ----------
        name : str
            name of the mesh
        mesh_container : ABCMesh, optional
            mesh to be added. If none is give,
            then an empty mesh is added.

        Returns
        ----------
        FileMesh
            The mesh newly added to the file.
            See get_mesh for more information.

        """
        if mesh.name in self._file.root.mesh:
            raise ValueError(
                'Mesh \'{n}\` already exists'.format(n=mesh.name))

        group = self._file.create_group('/mesh/', mesh.name)
        m = FileMesh(group, self._file)

        if mesh:
            # copy the contents of the mesh to the file
            for point in mesh.iter_points():
                m.add_point(point)
            for edge in mesh.iter_edges():
                m.add_edge(edge)
            for face in mesh.iter_faces():
                m.add_face(face)
            for cell in mesh.iter_cells():
                m.add_cell(cell)

        self._file.flush()
        return m

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
        try:
            group = self._file.root.particle_container._f_get_child(name)
            pc = FileParticleContainer(group, self._file)
            return pc
        except tables.NoSuchNodeError:
            raise ValueError(
                'Particle container \'{n}\` does not exist'.format(n=name))

    def get_mesh(self, name):
        """Get mesh from file.

        The returned mesh can be used to query
        and change the related data stored in the file. If the
        file has been closed then the mesh should no longer be used.

        Parameters
        ----------
        name : str
            name of the mesh to return
        """

        try:
            group = self._file.root.mesh._f_get_child(name)
            m = FileMesh(group, self._file)
            return m
        except tables.NoSuchNodeError:
            raise ValueError(
                'Mesh \'{n}\` does not exist'.format(n=name))

    def delete_particle_container(self, name):
        """Delete particle container from file.

        Parameters
        ----------
        name : str
            name of particle container to delete
        """
        try:
            pc_node = self._file.root.particle_container._f_get_child(name)
            pc_node._f_remove(recursive=True)
        except tables.NoSuchNodeError:
            raise ValueError(
                'Particle container \'{n}\` does not exist'.format(n=name))

    def delete_mesh(self, name):
        """Delete mesh from file.

        Parameters
        ----------
        name : str
            name of the mesh to delete
        """

        if name in self._meshes:
            self._meshes[name][1]._f_remove(recursive=True)
            del self._meshes[name]
        else:
            raise ValueError(
                'Mesh \'{n}\` does not exist'.format(n=name))

    def iter_particle_containers(self, names=None):
        """Returns an iterator over a subset or all
        of the particle containers.

        Parameters
        ----------
        names : list of str
            names of specific particle containers to be iterated over.
            If names is not given, then all particle containers will
            be iterated over.

        """
        names = copy.deepcopy(names)
        if names is None:
            for pc_node in self._file.root.particle_container._f_iter_nodes():
                yield self.get_particle_container(pc_node._v_name)
        else:
            for name in names:
                yield self.get_particle_container(name)

    def iter_mesh(self, names=None):
        """Returns an iterator over a subset or all
        of the meshes.

        Parameters
        ----------
        names : list of str
            names of specific meshes to be iterated over.
            If names is not given, then all meshes will
            be iterated over.

        """

        if names is None:
            for mesh_node in self._file.root.mesh._f_iter_nodes():
                yield self.get_mesh(mesh_node._v_name)
        else:
            for name in names:
                yield self.get_mesh(name)
