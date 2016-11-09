import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_component import CUDSComponent
from . import validation


class Boundary(CUDSComponent):
    '''System boundary  # noqa
    '''

    cuba_key = CUBA.BOUNDARY

    def __init__(self, condition, data=None, description="", name=""):

        self.condition = condition
        self.name = name
        self.description = description
        if data:
            internal_data = self.data
            internal_data.update(data)
            self.data = internal_data

        # This is a system-managed, read-only attribute
        self._definition = 'System boundary'  # noqa

    @property
    def condition(self):
        return self.data[CUBA.CONDITION]

    @condition.setter
    def condition(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'condition')
            validation.check_shape(value, '(:)')
            for item in value:
                validation.validate_cuba_keyword(item, 'condition')
        data = self.data
        data[CUBA.CONDITION] = value
        self.data = data

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer()
            data_container = self._data

        return DataContainer(data_container)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

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
        return (CUBA.DESCRIPTION, CUBA.UUID, CUBA.CONDITION, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
