import uuid
from simphony.core import data_container as dc
from simphony.core import cuba as cb
from .computational_method import ComputationalMethod
from . import validation


class IntegrationTime(ComputationalMethod):

    '''the current time, time step, and final time for a simulation stored on each cuds (a specific state).  # noqa
    '''

    cuba_key = cb.CUBA.INTEGRATION_TIME

    def __init__(self, description=None, name=None, data=None, current=0.0, size=0.0, final=0.0):

        self.description = description
        self.name = name
        if data:
            self.data = data
        self.current = current
        self.size = size
        self.final = final
        # This is a system-managed, read-only attribute
        self._definition = 'the current time, time step, and final time for a simulation stored on each cuds (a specific state).'  # noqa
        # This is a system-managed, read-only attribute
        self._physics_equation = []

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = dc.DataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, dc.DataContainer):
                raise TypeError("data is not a DataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, dc.DataContainer):
            self._data = new_data
        else:
            self._data = dc.DataContainer(new_data)

    @property
    def current(self):
        return self.data[cb.CUBA.CURRENT]

    @current.setter
    def current(self, value):
        value = validation.cast_data_type(value, 'current')
        validation.validate_cuba_keyword(value, 'current')
        self.data[cb.CUBA.CURRENT] = value

    @property
    def size(self):
        return self.data[cb.CUBA.SIZE]

    @size.setter
    def size(self, value):
        value = validation.cast_data_type(value, 'size')
        validation.validate_cuba_keyword(value, 'size')
        self.data[cb.CUBA.SIZE] = value

    @property
    def final(self):
        return self.data[cb.CUBA.FINAL]

    @final.setter
    def final(self, value):
        value = validation.cast_data_type(value, 'final')
        validation.validate_cuba_keyword(value, 'final')
        self.data[cb.CUBA.FINAL] = value

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
        return (cb.CUBA.CURRENT, cb.CUBA.UUID, cb.CUBA.DESCRIPTION, cb.CUBA.PHYSICS_EQUATION, cb.CUBA.SIZE, cb.CUBA.FINAL, cb.CUBA.NAME)

    @classmethod
    def parents(cls):
        return (cb.CUBA.COMPUTATIONAL_METHOD, cb.CUBA.CUDS_COMPONENT, cb.CUBA.CUDS_ITEM)
