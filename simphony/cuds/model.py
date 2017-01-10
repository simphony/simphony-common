"""CUDS computational model implementation.

This module contains the classes used to represent a computational model,
based on SimPhoNy metadata.
"""
import uuid

from simphony.cuds.utils import deprecated
from .store import MemoryStateDataStore
from .abc_particles import ABCParticles
from .abc_lattice import ABCLattice
from .abc_mesh import ABCMesh
from .meta import api
from ..core import DataContainer


class CUDS(object):
    """Common Universal Data Structure, i.e. CUDS computational model.

    This is the main data structure to hold all the information regarding
    a computational model. Having the data provided by this class, one should
    be able to start a new computational model based on that with no extra
    information.

    Parameters
    ----------
    name: str
        Name of this CUDS
    description: str
        More information about this CUDS
    """
    def __init__(self, name=None, description=None):

        # Assign unique ID
        self._uid = uuid.uuid4()

        # Add name
        self.name = name

        # Add description
        self.description = description

        # Add datasets to memory datastore by default
        self._dataset_store = MemoryStateDataStore()

        # Memory storage to keep CUDS components
        self._store = {}

        # The generic data container
        self._data = DataContainer()

        # A map to find the object for a given id among datasets or
        # simple components. Unfortunately, at the moment dataset
        # containers do not have `uid' and therefore this workaround
        # is necessary. This is a dict of key of any kind and a lambda
        # that will return the corresponding value.
        self._map = {}

        # Another map to keep a mapping between names and ids
        self._name_to_id_map = {}

    @property
    def uid(self):
        return self._uid

    @staticmethod
    def _is_dataset(obj):
        """Check if the object is a dataset."""
        return isinstance(obj, (ABCParticles,
                                ABCLattice,
                                ABCMesh,
                                api.DataSet))

    @property
    def data(self):
        """Data container for CUDS items."""
        return DataContainer(self._data)

    @data.setter
    def data(self, value):
        self._data = DataContainer(value)

    def add(self, component):
        """Add a component to the CUDS computational model.

        This will replace any existing value with the same `uid`.

        Parameters
        ----------
        component: CUDSComponent
            a CUDS component according to the SimPhoNy metadata

        Raises
        ------
        TypeError
            if the component is not a CUDS component
        ValueError
            if a component with the same name already exists
        """
        # Only accept CUDSComponent subclasses and datasets
        if not (isinstance(component, api.CUDSComponent) or
                self._is_dataset(component)):
            raise TypeError('Not a CUDSComponent nor a dataset object: %s.' %
                            type(component))

        # Do not accept items with duplicate names.
        # Components/datasets with no name will be added, however
        # it is not possible to get/remove them with `name`
        if component.name in self._name_to_id_map:
            raise ValueError('Name clash. Component with uid `%s`'
                             ' is already named `%s`'
                             % (self._name_to_id_map[component.name],
                                component.name))

        # Add datasets separately
        if self._is_dataset(component):
            if not component.name:
                raise TypeError('Dataset must have a name.')

            self._dataset_store.add(component)
            # Datasets at the moment do not have uid
            self._map[component.name] = \
                lambda key=component.name: self._dataset_store.get(key)
            # Datasets use name as id
            self._name_to_id_map[component.name] = component.name
        else:
            # Delete existing item with the same name
            # Store the component. Any CUDS item has uid property.
            self._store[component.uid] = component
            self._map[component.uid] = \
                lambda key=component.uid: self._store.get(key)
            # Store name for name-to-id mapping.
            # Components with no name will are not added to the mapping
            # and it is not possible to access them using add/remove
            # methods. Use `get_by_uid` and `remove_by_uid` instead.
            if component.name not in (None, ''):
                self._name_to_id_map[component.name] = component.uid

    def get(self, name):
        """Get the corresponding component from the CUDS computational model.

        Parameters
        ----------
        name: str
            name of the component

        Returns
        -------
        component: CUDSComponent
            the corresponding CUDS component or None

        Raises
        ------
        TypeError
            if the name is not a non empty string
        """
        if not name:
            raise TypeError('name must be a non empty string.')

        uid = self._name_to_id_map.get(name)
        return self.get_by_uid(uid)

    def get_by_uid(self, uid):
        """Get the corresponding component from the CUDS computational model.

        Parameters
        ----------
        uid: uuid.UUID
            uid of the component

        Returns
        -------
        component: CUDSComponent
            the corresponding CUDS component
        """
        if uid in self._map:
            return self._map[uid]()

    def remove(self, name):
        """Remove the corresponding component from the CUDS computational model.

        Parameters
        ----------
        name: str
            name of the component to be removed

        Raises
        ------
        KeyError
            if no component exists of the given name

        TypeError
            if the name is not a non empty string
        """
        if not name:
            raise TypeError('name must be a non empty string.')

        uid = self._name_to_id_map.get(name)
        self.remove_by_uid(uid)

        # Delete object's key from the mapping
        if name in self._name_to_id_map:
            del self._name_to_id_map[name]

    def remove_by_uid(self, uid):
        """Remove the corresponding component from the CUDS computational model.

        Parameters
        ----------
        uid: uuid.UUID
            uid of the component to be removed

        Raises
        ------
        KeyError
            if no component exists of the given uid
        """
        component = self.get_by_uid(uid)
        if not component:
            raise KeyError('No component exists for %s' % uid)
        if self._is_dataset(component):
            self._dataset_store.remove(component.name)
        else:
            del self._store[uid]
        # Delete object key from the mappings
        if component.name in self._name_to_id_map:
            del self._name_to_id_map[component.name]

    # This should be query method
    def iter(self, component_type):
        """Returns an iterator for the components of the given type.

        Parameters
        ----------
        component_type: CUDSComponent class
            a component of CUDS, reflecting SimPhoNy metadata

        Yields
        ------
        iterator over the components of the given type
        """
        values = None
        if issubclass(component_type, (ABCParticles, ABCLattice, ABCMesh)):
            values = self._dataset_store.iter_datasets()
        else:
            values = self._store.itervalues()

        for component in values:
            if isinstance(component, component_type):
                yield component

    def get_names(self, component_type):
        """Get names of the components of the given type.

        Parameters
        ----------
        component_type: CUDSComponent class
            a component of CUDS, reflecting SimPhoNy metadata

        Returns
        -------
        names: list
            names of the items of the given type
        """
        if any([issubclass(component_type, ABCParticles),
                issubclass(component_type, ABCLattice),
                issubclass(component_type, ABCMesh)]):
            return self._dataset_store.get_names()
        else:
            return [cp.name for cp in self._store.itervalues()
                    if isinstance(cp, component_type)]
