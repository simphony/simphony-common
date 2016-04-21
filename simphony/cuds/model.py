"""CUDS computational model implementation.

This module contains the classes used to represent a computational model,
based on SimPhoNy metadata.
"""
import uuid

from ..core import DataContainer
from .store import MemoryStateDataStore
from .abc_particles import ABCParticles
from .abc_lattice import ABCLattice
from .abc_mesh import ABCMesh


# IDEA: add consistency check handlers/instances to the CUDS class (dynamic).
class CUDS(object):
    """Common Universal Data Structure, i.e. CUDS computational model.

    This is the main data structure to hold all the information regarding
    a computational model. Having the data provided by this class, one should
    be able to start a new computational model based on that with no extra
    information.
    """
    def __init__(self):

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

    @staticmethod
    def _is_cuds_component(obj):
        """Check whether the object is a CUDS component."""
        # When I see a bird that walks like a duck and swims like a duck
        # and quacks like a duck, I call that bird a duck
        # TODO: replace with metadata type checks
        return all([hasattr(obj, 'name'),
                    hasattr(obj, 'data')])

    @staticmethod
    def _is_dataset(obj):
        """Check if the object is a dataset."""
        return isinstance(obj, (ABCParticles, ABCLattice, ABCMesh))

    @property
    def data(self):
        """Data container for CUDS items."""
        return DataContainer(self._data)

    @data.setter
    def data_setter(self, value):
        self._data = DataContainer(value)

    def add(self, component):
        """Add a component to the CUDS computational model.

        Parameters
        ----------
        component: CUDSComponent
            a component of CUDS, reflecting SimPhoNy metadata
        """
        # Check if the object is valid
        if not self._is_cuds_component(component):
            raise ValueError('Not a CUDS component.')

        # Add datasets separately
        if self._is_dataset(component):
            self._dataset_store.add(component)
            # Datasets have a uuid field called uid
            self._map[component.name] = \
                lambda key=component.name: self._dataset_store.get(key)
        else:
            # Store the component. Any cuds item has uuid property.
            component_id = str(component.uuid)
            self._store[component_id] = component
            self._map[component_id] = \
                lambda key=component_id: self._store.get(key)

    def get(self, component_id):
        """Gets a component from the CUDS computational model.

        Parameters
        ----------
        component_id: uuid.UUID
            key of a CUDS component

        Returns
        -------
        component: CUDSComponent
            a cuds component
        """
        if not isinstance(component_id, (str, uuid.UUID)):
            raise TypeError('ID should be of string or UUID type')
        if isinstance(component_id, uuid.UUID):
            component_id = str(component_id)
        if component_id in self._map:
            return self._map[component_id]()

    def remove(self, component_id):
        """Removes a component from the CUDS computational model.

        Parameters
        ----------
        component_id: uuid.UUID
            a component of CUDS, reflecting SimPhoNy metadata
        """
        if not isinstance(component_id, (str, uuid.UUID)):
            raise TypeError('ID should be of string or UUID type')
        if isinstance(component_id, uuid.UUID):
            component_id = str(component_id)

        component = self.get(component_id)
        if not component:
            raise KeyError('%s' % component_id)
        if self._is_dataset(component):
            self._dataset_store.remove(component.name)
        else:
            del self._store[component_id]

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
        for component in self._store.itervalues():
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
