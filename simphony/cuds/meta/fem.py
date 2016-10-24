import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .computational_method import ComputationalMethod


class Fem(ComputationalMethod):

    '''Finite element method  # noqa
    '''

    cuba_key = CUBA.FEM

    def __init__(self, data=None, description=None, name=None):

        if data:
            self.data = data
        self.description = description
        self.name = name
        # This is a system-managed, read-only attribute
        self._physics_equation = [CUBA.CFD]
        # This is a system-managed, read-only attribute
        self._definition = 'Finite element method'  # noqa

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer.new_with_restricted_keys(
                self.supported_parameters())
            data_container = self._data

        # One more check in case the
        # property setter is by-passed
        if not isinstance(data_container, DataContainer):
            raise TypeError("data is not a DataContainer. "
                            "data.setter is by-passed.")

        retvalue = DataContainer.new_with_restricted_keys(
            self.supported_parameters()
            )
        retvalue.update(data_container)

        return retvalue

    @data.setter
    def data(self, new_data):
        data = DataContainer.new_with_restricted_keys(
            self.supported_parameters()
            )
        data.update(new_data)
        self._data = data

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
