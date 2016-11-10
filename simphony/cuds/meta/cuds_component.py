import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem
from . import validation


class CUDSComponent(CUDSItem):
    '''Base data type for the CUDS components  # noqa
    '''

    cuba_key = CUBA.CUDS_COMPONENT

    def __init__(self, data=None, description="", name=""):

        self._data = DataContainer()

        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._definition = 'Base data type for the CUDS components'  # noqa

    @property
    def name(self):
        return self.data[CUBA.NAME]

    @name.setter
    def name(self, value):
        value = validation.cast_data_type(value, 'name')
        validation.validate_cuba_keyword(value, 'name')
        data = self.data
        data[CUBA.NAME] = value
        self.data = data

    @property
    def description(self):
        return self.data[CUBA.DESCRIPTION]

    @description.setter
    def description(self, value):
        value = validation.cast_data_type(value, 'description')
        validation.validate_cuba_keyword(value, 'description')
        data = self.data
        data[CUBA.DESCRIPTION] = value
        self.data = data

    @property
    def data(self):
        return DataContainer(self._data)

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
        return (CUBA.UUID, CUBA.DESCRIPTION, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_ITEM, )
