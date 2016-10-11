import uuid
from simphony.core import data_container as dc
from simphony.core import cuba as cb
from .condition import Condition
from . import validation


class Empty(Condition):

    '''Empty boundary condition  # noqa
    '''

    cuba_key = cb.CUBA.EMPTY

    def __init__(self, description=None, name=None, data=None, variable=None, material=None):

        self.description = description
        self.name = name
        if data:
            self.data = data
        if variable is None:
            self.variable = []
        if material is None:
            self.material = []
        # This is a system-managed, read-only attribute
        self._models = [cb.CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'Empty boundary condition'  # noqa

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
    def variable(self):
        return self.data[cb.CUBA.VARIABLE]

    @variable.setter
    def variable(self, value):
        value = validation.cast_data_type(value, 'variable')
        validation.check_shape(value, '(:)')
        for item in value:
            validation.validate_cuba_keyword(item, 'variable')
        self.data[cb.CUBA.VARIABLE] = value

    @property
    def material(self):
        return self.data[cb.CUBA.MATERIAL]

    @material.setter
    def material(self, value):
        value = validation.cast_data_type(value, 'material')
        validation.check_shape(value, '(:)')
        for item in value:
            validation.validate_cuba_keyword(item, 'material')
        self.data[cb.CUBA.MATERIAL] = value

    @property
    def models(self):
        return self._models

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
        return (cb.CUBA.DESCRIPTION, cb.CUBA.VARIABLE, cb.CUBA.MATERIAL, cb.CUBA.UUID, cb.CUBA.NAME)

    @classmethod
    def parents(cls):
        return (cb.CUBA.CONDITION, cb.CUBA.CUDS_COMPONENT, cb.CUBA.CUDS_ITEM)
