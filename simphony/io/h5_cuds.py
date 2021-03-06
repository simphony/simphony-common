import tables
import itertools

from ..core import CUBA
from ..core.data_container import DataContainer
from ..cuds import ABCParticles, ABCMesh, ABCLattice
from .h5_particles import H5Particles
from .h5_mesh import H5Mesh
from .h5_lattice import H5Lattice

H5_FILE_VERSION = 3


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
    def open(cls, filename, mode="a", title='', filters=None):
        """ Returns an opened SimPhoNy CUDS-hdf5 file

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

        filters : tables.Filter
            Filter options used in the HDF5 file. If none is selected
            default parameters are: complevel=1, complib="zlib" and
            fletcher32=True. This only applies to newly created files.

        Raises
        ------
        ValueError :
            If the file has an incompatible version

        """

        if filters is None:
            filters = tables.Filters(
                complevel=1,
                complib='zlib',
                fletcher32=True
            )

        handle = tables.open_file(
            filename,
            mode,
            title=title,
            filters=filters
        )

        if handle.list_nodes("/"):
            if not ("cuds_version" in handle.root._v_attrs and
                    handle.root._v_attrs.cuds_version == H5_FILE_VERSION):
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

    def add_dataset(self, container, cuba_keys=None):
        """Add a CUDS container

        Parameters
        ----------
        container : {ABCMesh, ABCParticles, ABCLattice}
            The CUDS container to be added.
        cuba_keys : dict of CUBAs (optional)
            Dictionary of CUBAs with lists of CUBA keys that
            are added to the H5CUDS container. All keys in the container
            are stored by default

        Raises
        ------
        TypeError:
            If the container type is not supported by the file.
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
            self._add_particles(container, cuba_keys)
        elif isinstance(container, ABCMesh):
            self._add_mesh(container, cuba_keys)
        elif isinstance(container, ABCLattice):
            self._add_lattice(container, cuba_keys)
        else:
            raise TypeError(
                "The type of the container is not supported")

    def remove_dataset(self, name):
        """ Remove a dataset from the file

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

    def get_dataset_names(self):
        """ Returns a list of the datasets' names contained in the file.

        """

        ip = self._iter_particles()
        im = self._iter_meshes()
        il = self._iter_lattices()

        iter_list = itertools.chain(ip, im, il)

        return [i.name for i in iter_list]

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

    def _add_particles(self, particles, cuba_keys):
        """Add particle container to the file.

        Parameters
        ----------
        particles : ABCParticles
            Particle container to be added.
        cuba_keys : dict
            Dictionary of CUBAs with their related CUBA keys that
            are added to the H5CUDS container.

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

        if cuba_keys is not None:
            for item in particles.iter(item_type=CUBA.PARTICLE):
                item.data = DataContainer(
                    {key: item.data[key] for key in item.data
                     if key in cuba_keys[CUBA.PARTICLE]})
                h5_particles.add([item])

            for item in particles.iter(item_type=CUBA.BOND):
                item.data = DataContainer(
                    {key: item.data[key] for key in item.data
                     if key in cuba_keys[CUBA.BOND]})
                h5_particles.add([item])
        else:
            h5_particles.add(particles.iter())

    def _add_mesh(self, mesh, cuba_keys):
        """Add a mesh to the file.

        Parameters
        ----------
        mesh_container : ABCMesh, optional
            mesh to be added. If none is give,
            then an empty mesh is added.
        cuba_keys : dict
            Dictionary of CUBAs with their related CUBA keys that
            are added to the H5CUDS container.

        Returns
        ----------
        H5Mesh
            The mesh newly added to the file.

        """
        name = mesh.name
        mesh_root = self._root.mesh

        group = tables.Group(mesh_root, name=name, new=True)
        h5_mesh = H5Mesh(group, self._handle)
        h5_mesh.data = mesh.data

        if cuba_keys is not None:
            for item in mesh.iter(item_type=CUBA.POINT):
                item.data = DataContainer(
                    {key: item.data[key] for key in item.data
                     if key in cuba_keys[CUBA.POINT]})
                h5_mesh.add([item])

            for item in mesh.iter(item_type=CUBA.EDGE):
                item.data = DataContainer(
                    {key: item.data[key] for key in item.data
                     if key in cuba_keys[CUBA.EDGE]})
                h5_mesh.add([item])

            for item in mesh.iter(item_type=CUBA.FACE):
                item.data = DataContainer(
                    {key: item.data[key] for key in item.data
                     if key in cuba_keys[CUBA.FACE]})
                h5_mesh.add([item])

            for item in mesh.iter(item_type=CUBA.CELL):
                item.data = DataContainer(
                    {key: item.data[key] for key in item.data
                     if key in cuba_keys[CUBA.CELL]})
                h5_mesh.add([item])
        else:
            h5_mesh.add(mesh.iter())

    def _add_lattice(self, lattice, cuba_keys):
        """Add lattice to the file.

        Parameters
        ----------
        lattice : Lattice
            lattice to be added
        cuba_keys : dict
            Dictionary of CUBAs with their related CUBA keys that
            are added to the H5CUDS container.

        Returns
        ----------
        H5Lattice
            The lattice newly added to the file.

        """
        name = lattice.name
        lattice_root = self._root.lattice

        group = tables.Group(lattice_root, name=name, new=True)
        h5_lattice = H5Lattice.create_new(
            group, lattice.primitive_cell, lattice.size, lattice.origin)
        h5_lattice.data = lattice.data

        if cuba_keys is not None:
            for item in lattice.iter(item_type=CUBA.NODE):
                item.data = DataContainer(
                    {key: item.data[key] for key in item.data
                     if key in cuba_keys[CUBA.NODE]})
                h5_lattice.update([item])
        else:
            h5_lattice.update(lattice.iter(item_type=CUBA.NODE))

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
