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

        If the component has `uid` attribute but that value is
        None, a new uuid will be created and assigned to the
        component after the component is successfully added
        to the CUDS computational model.

        Parameters
        ----------
        component: CUDSComponent
            a component of CUDS, reflecting SimPhoNy metadata

        Raises
        ------
        TypeError
            if component is not a CUDS component

        ValueError
            if the component is already added
        """
        # Check if the object is valid
        if not self._is_cuds_component(component):
            raise TypeError('Not a CUDS component.')

        try:
            component_id = component.uuid
        except AttributeError:
            # Datasets (ABCParticles, ABCLattice, ABCMesh) do not
            # have a uid attibute
            component_id = component.name
        else:
            # if the uuid is not defined, create a new one here
            if component_id is None:
                component_id = uuid.uuid4()

        # Add datasets separately
        if self._is_dataset(component):
            self._dataset_store.add(component)
        else:
            # Store the component. Any cuds item has uuid property.
            self._store[component_id] = component

        # If the component already has a defined uid, this just reassigns
        # the same value.  If the component.uuid is originaly None, this
        # assigns the new uid to the component.uuid
        # Only do so after successfully adding the component
        if isinstance(component_id, uuid.UUID) and hasattr(component, "uid"):
            component.uuid = component_id

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
        for dataset in (self._dataset_store, self._store):
            try:
                return dataset[component_id]
            except KeyError:
                continue
        else:
            return None

    def remove(self, component_id):
        """Removes a component from the CUDS computational model.

        Parameters
        ----------
        component_id: uuid.UUID
            a component of CUDS, reflecting SimPhoNy metadata
        """
        for dataset in (self._dataset_store, self._store):
            try:
                del dataset[component_id]
                break
            except KeyError:
                continue
        else:
            raise KeyError('%s' % component_id)

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
