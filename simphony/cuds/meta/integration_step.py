import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .computational_method import ComputationalMethod
from . import validation


class IntegrationStep(ComputationalMethod):

    '''the current step, integration step, and final number of steps for a simulation stored on each cuds (a specific state).  # noqa
    '''

    cuba_key = CUBA.INTEGRATION_STEP

    def __init__(self, size, final, description=None, name=None, data=None, current=0):

        self.size = size
        self.final = final
        self.description = description
        self.name = name
        if data:
            self.data = data
        self.current = current
        # This is a system-managed, read-only attribute
        self._definition = 'the current step, integration step, and final number of steps for a simulation stored on each cuds (a specific state).'  # noqa
        # This is a system-managed, read-only attribute
        self._physics_equation = []

    @property
    def size(self):
        return self.data[CUBA.SIZE]

    @size.setter
    def size(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'size')
            validation.validate_cuba_keyword(value, 'size')
        data = self.data
        data[CUBA.SIZE] = value
        self.data = data

    @property
    def final(self):
        return self.data[CUBA.FINAL]

    @final.setter
    def final(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'final')
            validation.validate_cuba_keyword(value, 'final')
        data = self.data
        data[CUBA.FINAL] = value
        self.data = data

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer()
            data_container = self._data

        # One more check in case the
        # property setter is by-passed
        if not isinstance(data_container, DataContainer):
            raise TypeError("data is not a DataContainer. "
                            "data.setter is by-passed.")
        return DataContainer(data_container)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    @property
    def current(self):
        return self.data[CUBA.CURRENT]

    @current.setter
    def current(self, value):
        value = validation.cast_data_type(value, 'current')
        validation.validate_cuba_keyword(value, 'current')
        data = self.data
        data[CUBA.CURRENT] = value
        self.data = data

    @property
    def definition(self):
        return self._definition

    @property
    def physics_equation(self):
        return self._physics_equation

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.CURRENT, CUBA.UUID, CUBA.DESCRIPTION, CUBA.PHYSICS_EQUATION, CUBA.SIZE, CUBA.FINAL, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.COMPUTATIONAL_METHOD, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
