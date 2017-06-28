"""CUDS computational model implementation.

This module contains the classes used to represent a computational model,
based on SimPhoNy metadata.
"""
from .meta import api
from .utils import map_cuba_key_to_cuds_class
from .abc_dataset import ABCDataset
from ..core import CUBA, DataContainer


def is_dataset(obj):
    """Check if the object is a dataset."""
    return isinstance(obj, (ABCDataset, api.DataSet))


class CUDS(api.CUDS):
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
    def __init__(self, name='', description=''):

        # A dictionary to keep all CUDS
        self._store = {}

        # The generic data container
        self._data = DataContainer()

        # Another map to keep a mapping between names and uids
        self._name_uid_map = {}

        # Call parent
        super(CUDS, self).__init__(name=name, description=description)

    def add(self, components):
        """Add a number of components to the CUDS computational model.

        This will replace any existing value with the same `uid`.

        Parameters
        ----------
        component: list of CUDSComponents
            list of CUDS components according to the SimPhoNy metadata

        Raises
        ------
        TypeError
            if the component is not a CUDS component
        ValueError
            if a component with the same name already exists
        """
        for component in components:
            # Only accept CUDSComponent subclasses and datasets
            if not (isinstance(component, api.CUDSComponent) or
                    is_dataset(component)):
                raise TypeError('Not a CUDSComponent nor'
                                'a dataset object: %s.' %
                                type(component))

            # Do not accept items with duplicate names.
            # Components/datasets with no name will be added, however
            # it is not possible to get/remove them with `name`
            if component.name in self._name_uid_map:
                raise ValueError('Name clash. Component with uid `%s`'
                                 ' is already named `%s`'
                                 % (self._name_uid_map[component.name],
                                    component.name))

            # Make sure datasets have names
            if is_dataset(component):
                if not component.name:
                    raise TypeError('Dataset must have a name.')

                # self._dataset_store.add(component)

            # Add the component to the generic store
            self._store[component.uid] = component

            # Add the component to the data using its CUBA key
            self._data[component.cuba_key] = component

            # Keep a name:uid map
            # FIXME: if user changes the name, this will go out of sync
            if component.name not in (None, ''):
                self._name_uid_map[component.name] = component.uid

    def update(self, components):
        """Update existing components with provided ones.

        Parameters
        ----------
        components: list of CUDSComponents

        Raises
        ------
        ValueError :
            If any object inside the iterable does not exist.
        """
        for component in components:
            self._update(component)

    def _update(self, component):
        """Update a component"""
        if component.uid not in self._store:
            raise ValueError("Component {name}:{uid} does not exist."
                             .format(name=component.name, uid=component.uid))

        self._store[component.uid] = component

    def get_by_name(self, name):
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
        KeyError
            when no object with the given uid exists

        """
        if not name:
            raise TypeError('name must be a non empty string.')

        uid = self._name_uid_map.get(name)
        return self.get(uid)

    def get(self, uid):
        """Get the corresponding component from the CUDS computational model.

        Parameters
        ----------
        uid: uuid.UUID
            uid of the component

        Raises
        ------
        KeyError
            when no object with the given uid exists

        Returns
        -------
        component: CUDSComponent
            the corresponding CUDS component
        """
        if uid not in self._store:
            raise KeyError("No object found for uid: {uid}"
                           .format(uid=uid))

        return self._store.get(uid)

    def remove(self, uids):
        """Remove the corresponding component from the CUDS computational model.

        Parameters
        ----------
        uid: list of uuid.UUID
            uid of the components to be removed

        Raises
        ------
        KeyError
            if no component exists of the given uid
        """
        for uid in uids:
            component = self.get(uid)
            if not component:
                raise KeyError('No component exists for %s' % uid)

            # Delete the object from the internal store
            del self._store[uid]

            # Delete object key from the mappings
            if component.name in self._name_uid_map:
                del self._name_uid_map[component.name]

    # TODO: This should be a query method
    def iter(self, uids=None, item_type=None):
        """Returns an iterator for the components of the given type.

        Parameters
        ----------
        uids : iterable of uuid.UUID, optional
            sequence containing the uids of the objects that will be
            iterated. When the uids are provided, then the objects are
            returned in the same order the uids are returned by the iterable.
            If uids is None, then all objects are returned by the iterable
            and there is no restriction on the order that they are returned.

        item_type: CUBA
            Restricts iteration only to the specified CUBA.

        Raises
        ------
        KeyError
            if any of the ids passed as parameters are not in the container.

        Yields
        ------
        iterator over the components of the given type
        """
        if uids:
            if not all(uid in self._store for uid in uids):
                raise KeyError('No object exists for uid')
        else:
            uids = self._store.keys()

        # Get the equivalent class type for the key
        if item_type:
            # FIXME: dirty hack for now
            if item_type in (CUBA.PARTICLES, CUBA.LATTICE, CUBA.MESH):
                component_type = ABCDataset
            else:
                component_type = map_cuba_key_to_cuds_class(item_type)
        else:
            component_type = object

        for uid in uids:
            if isinstance(self._store[uid], component_type):
                yield self._store[uid]

    def has(self, uid):
        """Checks if an object with the given uid already exists
        in the dataset.

        Parameters
        ----------
        uid : uuid.UUID
            the uid of the object

        Returns
        -------
        True if the uid is found, False otherwise.
        """
        return uid in self._store

    def has_type(self, item_type):
        """Checks if the specified CUBA type is present
        in the dataset.

        Parameters
        ----------
        item_type : CUBA
            The CUBA enum of the type of the items to return the count of.

        Returns
        -------
        True if the type is present, False otherwise.
        """
        # Get the equivalent class type for the key
        component_type = map_cuba_key_to_cuds_class(item_type)

        for component in self._store.itervalues():
            if isinstance(component, component_type):
                return True
        return False

    def count_of(self, item_type):
        """Returns an iterator for the components of the given type.

        Parameters
        ----------
        item_type: CUBA
            Restricts iteration only to the specified CUBA.

        Yields
        ------
        iterator over the components of the given type
        """
        # Get the equivalent class type for the key
        component_type = map_cuba_key_to_cuds_class(item_type)

        length = 0
        for component in self._store.itervalues():
            if isinstance(component, component_type):
                length += 1
        return length

    def __len__(self):
        """Returns the total number of items in the container.

        Returns
        -------
        count : int
            The number of items in the dataset.
        """
        return len(self._store)

    def __contains__(self, item):
        """Implements the `in` interface. Behaves as the has() method.
        """
        return self.has(item)
