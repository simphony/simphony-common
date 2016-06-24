import uuid
from simphony.core.data_container import create_data_container
from simphony.core.cuba import CUBA
from .computational_method import ComputationalMethod

_RestrictedDataContainer = create_data_container(
    (CUBA.DESCRIPTION, CUBA.PHYSICS_EQUATION, CUBA.UUID, CUBA.NAME),
    class_name="_RestrictedDataContainer")


class Sph(ComputationalMethod):
    '''Smooth particle hydrodynamics  # noqa
    '''

    cuba_key = CUBA.SPH

    def __init__(self, description=None, name=None, data=None):

        self.description = description
        self.name = name
        if data:
            self.data = data

        # This is a system-managed, read-only attribute
        self._physics_equation = [CUBA.CFD]

        # This is a system-managed, read-only attribute
        self._definition = 'Smooth particle hydrodynamics'  # noqa

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = _RestrictedDataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, _RestrictedDataContainer):
                raise TypeError("data is not a RestrictedDataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, _RestrictedDataContainer):
            self._data = new_data
        else:
            self._data = _RestrictedDataContainer(new_data)

    @property
    def physics_equation(self):

        return self._physics_equation

    @property
    def definition(self):

        return self._definition

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.DESCRIPTION, CUBA.PHYSICS_EQUATION, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.COMPUTATIONAL_METHOD, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
