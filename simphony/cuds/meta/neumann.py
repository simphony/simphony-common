import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .condition import Condition
from . import validation


class Neumann(Condition):
    '''Neumann boundary condition  # noqa
    '''

    cuba_key = CUBA.NEUMANN

    def __init__(self,
                 description=None,
                 name=None,
                 data=None,
                 variable=None,
                 material=None):

        self.description = description
        self.name = name
        if data:
            self.data = data
        if variable is None:
            self.variable = []
        if material is None:
            self.material = []
        # This is a system-managed, read-only attribute
        self._models = [CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'Neumann boundary condition'  # noqa

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, DataContainer):
                raise TypeError("data is not a DataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, DataContainer):
            self._data = new_data
        else:
            self._data = DataContainer(new_data)

    @property
    def variable(self):
        return self.data[CUBA.VARIABLE]

    @variable.setter
    def variable(self, value):
        value = validation.cast_data_type(value, 'variable')
        validation.check_shape(value, '(:)')
        for item in value:
            validation.validate_cuba_keyword(item, 'variable')
        self.data[CUBA.VARIABLE] = value

    @property
    def material(self):
        return self.data[CUBA.MATERIAL]

    @material.setter
    def material(self, value):
        value = validation.cast_data_type(value, 'material')
        validation.check_shape(value, '(:)')
        for item in value:
            validation.validate_cuba_keyword(item, 'material')
        self.data[CUBA.MATERIAL] = value

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
        return (CUBA.DESCRIPTION, CUBA.VARIABLE, CUBA.MATERIAL, CUBA.UUID,
                CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CONDITION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
