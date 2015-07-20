import tables

from simphony.cuds.abstractparticles import ABCParticles
from simphony.cuds.abstractmesh import ABCMesh
from simphony.cuds.abstractlattice import ABCLattice

from simphony.io.h5_particles import H5Particles
from simphony.io.h5_mesh import H5Mesh
from simphony.io.h5_lattice import H5Lattice

H5_FILE_VERSION = 1


class H5CUDS(object):
    """ Access to CUDS-hdf5 formatted files.

    """

    def __init__(self, handle):
        """ Create/Open a CUDS file.

        Parameters
        ----------
        handle : table.file
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

        Raises              Raises
        ------
        ValueError :
            If the file has an incompatible version

        """
        handle = tables.open_file(filename, mode, title=title)

        if handle.list_nodes("/"):
            if not ("cuds_version" in handle.root._v_attrs
                    and handle.root._v_attrs.cuds_version == H5_FILE_VERSION):
                handle.close()
                raise ValueError("File version is incompatible")
        else:
            handle.root._v_attrs.cuds_version = H5_FILE_VERSION
            for group in ('particle', 'lattice', 'mesh'):
                if "/" + group not in handle:
                    handle.create_group('/', group, group)
        return cls(handle)

    def close(self):
        """Closes a file

        """
        self._handle.close()

    def add_dataset(self, container):
        """Add a CUDS container

        Parameters
        ----------
        container : {ABCMesh, ABCParticles, ABCLattice}
            The CUDS container to be added.

        Raises
        ------
        TypeError:
            If the container type is not supported by the engine.
        ValueError:
            If there is already a dataset with the given name.

        """
        name = container.name
        message = '{} container {!r} already exists'

        if name in self._root.particle:
            raise ValueError(message.format('Particles', name))
        if name in self._root.mesh:
            raise ValueError(message.format('Mesh', name))
        if name in self._root.lattice:
            raise ValueError(message.format('Lattice', name))

        if isinstance(container, ABCParticles):
            self._add_particles(container)
        elif isinstance(container, ABCMesh):
            self._add_mesh(container)
        elif isinstance(container, ABCLattice):
            self._add_lattice(container)
        else:
            raise TypeError(
                "The type of the container is not supported")

    def remove_dataset(self, name):
        """ Remove a dataset from the engine

        Parameters
        ----------
        name: str
            name of CUDS container to be deleted

        Raises
        ------
        ValueError:
            If there is no dataset with the given name

        """
        if name in self._get_child_names(self._root.particle):
            self._remove_particles(name)
        elif name in self._get_child_names(self._root.mesh):
            self._remove_mesh(name)
        elif name in self._get_child_names(self._root.lattice):
            self._remove_lattice(name)
        else:
            raise ValueError(
                'Container \'{n}\` does not exist'.format(n=name))

    def get_dataset(self, name):
        """ Get the dataset

        Parameters
        ----------
        name: str
            name of CUDS container to be retrieved.

        Returns
        -------
        container :
            A proxy of the dataset named ``name`` that is stored
            internally in the File.

        Raises
        ------
        ValueError:
            If there is no dataset with the given name

        """
        if name in self._get_child_names(self._root.particle):
            return self._get_particles(name)
        elif name in self._get_child_names(self._root.mesh):
            return self._get_mesh(name)
        elif name in self._get_child_names(self._root.lattice):
            return self._get_lattice(name)
        else:
            raise ValueError(
                'Container \'{n}\` does not exist'.format(n=name))

    def iter_datasets(self, names=None):
        """ Returns an iterator over a subset or all of the containers.

        Parameters
        ----------
        names : sequence of str, optional
            names of specific containers to be iterated over. If names is not
            given, then all containers will be iterated over.

        """

        ip = self._iter_particles(names)
        im = self._iter_meshes(names)
        il = self._iter_lattices(names)

        iter_list = [i for i in ip] + [i for i in im] + [i for i in il]

        if names is not None:
            for name in names:
                if name not in [i.name for i in iter_list]:
                    raise ValueError(
                        'Container \'{n}\` does not exist'.format(n=name))
        for i in iter_list:
            yield i

    def _get_child_names(self, node):
        return [n._v_name for n in node._f_iter_nodes()]

    def _add_particles(self, particles):
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

        group = tables.Group(particles_root, name=name, new=True)
        h5_particles = H5Particles(group)
        h5_particles.data = particles.data
        h5_particles.add_particles(particles.iter_particles())
        h5_particles.add_bonds(particles.iter_bonds())

    def _add_mesh(self, mesh):
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
        name = mesh.name
        mesh_root = self._root.mesh

        group = tables.Group(mesh_root, name=name, new=True)
        h5_mesh = H5Mesh(group, self._handle)
        h5_mesh.data = mesh.data
        h5_mesh.add_points(mesh.iter_points())
        h5_mesh.add_edges(mesh.iter_edges())
        h5_mesh.add_faces(mesh.iter_faces())
        h5_mesh.add_cells(mesh.iter_cells())

    def _add_lattice(self, lattice):
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
        name = lattice.name
        lattice_root = self._root.lattice

        group = tables.Group(lattice_root, name=name, new=True)
        h5_lattice = H5Lattice.create_new(
            group, lattice.type, lattice.base_vect,
            lattice.size, lattice.origin)
        h5_lattice.data = lattice.data
        h5_lattice.update_nodes(lattice.iter_nodes())

    def _get_particles(self, name):
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
        group = self._root.particle._f_get_child(name)
        return H5Particles(group)

    def _get_mesh(self, name):
        """Get mesh from file.

        The returned mesh can be used to query
        and change the related data stored in the file. If the
        file has been closed then the mesh should no longer be used.

        Parameters
        ----------
        name : str
            name of the mesh to return
        """
        group = self._root.mesh._f_get_child(name)
        return H5Mesh(group, self._handle)

    def _get_lattice(self, name):
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
        group = self._root.lattice._f_get_child(name)
        return H5Lattice(group)

    def _remove_particles(self, name):
        """Delete particle container from file.

        Parameters
        ----------
        name : str
            name of particle container to delete
        """
        node = self._root.particle._f_get_child(name)
        node._f_remove(recursive=True)

    def _remove_mesh(self, name):
        """Delete mesh from file.

        Parameters
        ----------
        name : str
            name of the mesh to delete
        """
        node = self._root.mesh._f_get_child(name)
        node._f_remove(recursive=True)

    def _remove_lattice(self, name):
        """Delete lattice from file.

        Parameters
        ----------
        name : str
            name of lattice to delete
        """
        node = self._root.lattice._f_get_child(name)
        node._f_remove(recursive=True)

    def _iter_particles(self, names=None):
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
                yield self._get_particles(node._v_name)
        else:
            for name in names:
                if name in self._get_child_names(self._root.particle):
                    yield self._get_particles(name)

    def _iter_meshes(self, names=None):
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
                yield self._get_mesh(mesh_node._v_name)
        else:
            for name in names:
                if name in self._get_child_names(self._root.mesh):
                    yield self._get_mesh(name)

    def _iter_lattices(self, names=None):
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
                yield self._get_lattice(lattice._v_name)
        else:
            for name in names:
                if name in self._get_child_names(self._root.lattice):
                    yield self._get_lattice(name)
