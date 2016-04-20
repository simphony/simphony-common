"""CUDS computational model implementation.

This module contains the classes used to represent a computational model,
based on SimPhoNy metadata.
"""
from ..core import DataContainer
from .store import MemoryStateDataStore


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

        # Data container
        self._data = DataContainer()

    @staticmethod
    def _is_cuds_component(obj):
        """Check whether the object is a CUDS component."""
        # When I see a bird that walks like a duck and swims like a duck
        # and quacks like a duck, I call that bird a duck
        # TODO: replace with metadata type checks
        return all([hasattr(obj, 'name'),
                    hasattr(obj, 'data')])

    @property
    def data(self):
        """Data container for CUDS items."""
        return DataContainer(self._data)

    @data.setter
    def data_setter(self, value):
        self._data = DataContainer(value)

    def add(self, component):
        """Adds a component to the CUDS computational model.

        Parameters
        ----------
        component: CUDSComponent
            a component of CUDS, reflecting SimPhoNy metadata
        """
        # Check if the object is valid
        if not self._is_cuds_component(component):
            raise ValueError('Not a CUDS component.')

        # Store the component
        # TODO: use uuid of the component - does not exist yet
        self._store[id(component)] = component

    def get(self, component_id):
        """Gets a component from the CUDS computational model.

        Parameters
        ----------
        component_id: CUDSComponent's UUID
            uuid of a CUDS component.
        """
        return self._store.get(component_id)

    def remove(self, component_id):
        """Removes a component from the CUDS computational model.

        Parameters
        ----------
        component_id: CUDSComponent uuid
            a component of CUDS, reflecting SimPhoNy metadata
        """
        self._store.remove(component_id)

    # This should be query method
    def iter(self, component_type):
        """Returns an iterator for the components of the given type.

        Parameters
        ----------
        component_type: CUDSComponent class
            a component of CUDS, reflecting SimPhoNy metadata
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
        """
        for component in self._store.iteritems():
            if isinstance(component, component_type):
                yield component.name
