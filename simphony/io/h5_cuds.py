import tables

from simphony.io.h5_particles import H5Particles
from simphony.io.h5_mesh import H5Mesh
from simphony.io.h5_lattice import H5Lattice


class H5CUDS(object):
    """ Access to CUDS-hdf5 formatted files.

    """

    def __init__(self, handle):
        """ Create/Open a CUDS file.

        Parameters
        ----------
        file : table.file
            file to be used

        """
        if not isinstance(handle, tables.File):
            raise ValueError("File should be a Pytable file")
        self._handle = handle
        self._root = handle.root

    def valid(self):
        """Checks if file is valid (i.e. open)

        """
        return self._handle is not None and self._handle.isopen

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
            - ``r`` -- ReadOnly; This is a very restrictive mode that
              will through errors at any attempt to modify the data.

        title : str
            Title attribute of root node (only applies to a file which
              is being created)

        """
        handle = tables.open_file(filename, mode, title=title)
        # create the high-level structure of the cuds file
        for group in ('particle', 'lattice', 'mesh'):
            if "/" + group not in handle:
                handle.create_group('/', group, group)
        return cls(handle)

    def close(self):
        """Closes a file

        """
        self._handle.close()

    def add_particles(self, particles):
        """Add particle container to the file.

        Parameters
        ----------
        particles : ABCParticles
            Particle container to be added.

        Returns
        -------
        particles : H5Particles
            A newly created container proxying the data in the HDF5 file.

        """
        name = particles.name
        particles_root = self._root.particle
        if name in particles_root:
            message = 'Particles container {!r} already exists'
            raise ValueError(message.format(name))

        group = tables.Group(particles_root, name=name, new=True)
        h5_particles = H5Particles(group)
        # Set the data value of the newly created h5_particles object
        #  which will store it to the file
        h5_particles.data = particles.data

        # copy the contents of the particle container to the file
        for particle in particles.iter_particles():
            h5_particles.add_particle(particle)
        for bond in particles.iter_bonds():
            h5_particles.add_bond(bond)

        return h5_particles

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
        H5Mesh
            The mesh newly added to the file.
            See get_mesh for more information.

        """
        if mesh.name in self._root.mesh:
            raise ValueError(
                'Mesh \'{n}\` already exists'.format(n=mesh.name))

        group = self._handle.create_group('/mesh/', mesh.name)
        h5_mesh = H5Mesh(group, self._handle)

        if mesh:
            # copy the contents of the mesh to the file
            for point in mesh.iter_points():
                h5_mesh.add_point(point)
            for edge in mesh.iter_edges():
                h5_mesh.add_edge(edge)
            for face in mesh.iter_faces():
                h5_mesh.add_face(face)
            for cell in mesh.iter_cells():
                h5_mesh.add_cell(cell)

        self._handle.flush()
        return h5_mesh

    def add_lattice(self, lattice):
        """Add lattice to the file.

        Parameters
        ----------
        lattice : Lattice
            lattice to be added

        Returns
        ----------
        H5Lattice
            The lattice newly added to the file.

        """
        if lattice.name in self._root.lattice:
            raise ValueError(
                'Lattice \'{n}\` already exists'.format(n=lattice.name))

        group = self._handle.create_group('/lattice/', lattice.name)

        # Create a h5_lattice with all CUBA-keys defined
        h5lat = H5Lattice.create_new(group, lattice.type, lattice.base_vect,
                                     lattice.size, lattice.origin)

        # Copy the contents of the lattice to the file
        for node in lattice.iter_nodes():
            h5lat.update_node(node)

        # Copy lattice high level data to the file
        h5lat.data = {k: lattice.data[k] for k in lattice.data}
        self._handle.flush()

        return h5lat

    def get_particles(self, name):
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
            group = self._root.particle._f_get_child(name)
            return H5Particles(group)
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
            group = self._root.mesh._f_get_child(name)
            m = H5Mesh(group, self._handle)
            return m
        except tables.NoSuchNodeError:
            raise ValueError(
                'Mesh \'{n}\` does not exist'.format(n=name))

    def get_lattice(self, name):
        """Get lattice from file.

        The returned lattice can be used to query
        and change the related data stored in the file. If the
        file has been closed then the lattice should
        no longer be used.

        Parameters
        ----------
        name : str
            name of lattice to return
        """
        try:
            group = self._root.lattice._f_get_child(name)
            h5lat = H5Lattice(group)
            return h5lat
        except tables.NoSuchNodeError:
            raise ValueError(
                'Lattice \'{n}\` does not exist'.format(n=name))

    def delete_particles(self, name):
        """Delete particle container from file.

        Parameters
        ----------
        name : str
            name of particle container to delete
        """
        try:
            pc_node = self._root.particle._f_get_child(name)
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

        try:
            m_node = self._root.mesh._f_get_child(name)
            m_node._f_remove(recursive=True)
        except tables.NoSuchNodeError:
            raise ValueError(
                'Mesh \'{n}\` does not exist'.format(n=name))

    def delete_lattice(self, name):
        """Delete lattice from file.

        Parameters
        ----------
        name : str
            name of lattice to delete
        """
        try:
            h5lat = self._root.lattice._f_get_child(name)
        except tables.NoSuchNodeError:
            raise ValueError('Lattice \'{n}\` does not exist'.format(n=name))
        else:
            h5lat._f_remove(recursive=True)

    def iter_particles(self, names=None):
        """Returns an iterator over a subset or all
        of the particle containers.
        Parameters
        ----------
        names : list of str
            names of specific particle containers to be iterated over.
            If names is not given, then all particle containers will
            be iterated over.

        """
        if names is None:
            for node in self._root.particle._f_iter_nodes():
                yield self.get_particles(node._v_name)
        else:
            for name in names:
                yield self.get_particles(name)

    def iter_meshes(self, names=None):
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
            for mesh_node in self._root.mesh._f_iter_nodes():
                yield self.get_mesh(mesh_node._v_name)
        else:
            for name in names:
                yield self.get_mesh(name)

    def iter_lattices(self, names=None):
        """Returns an iterator over a subset or all
        of the lattices.

        Parameters
        ----------
        names : list of str
            names of specific lattices to be iterated over.
            If names is not given, then all lattices will
            be iterated over.

        """
        if names is None:
            for lattice in self._root.lattice._f_iter_nodes():
                yield self.get_lattice(lattice._v_name)
        else:
            for name in names:
                yield self.get_lattice(name)
