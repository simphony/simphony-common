import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem
from . import validation


class CUDSComponent(CUDSItem):
    '''Base data type for the CUDS components  # noqa
    '''

    cuba_key = CUBA.CUDS_COMPONENT

    def __init__(self, data=None, description=None, name=None):

        if data:
            self.data = data
        self.description = description
        self.name = name
        # This is a system-managed, read-only attribute
        self._definition = 'Base data type for the CUDS components'  # noqa

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
            self.supported_parameters())
        retvalue.update(data_container)

        return retvalue

    @data.setter
    def data(self, new_data):
        data = DataContainer.new_with_restricted_keys(
            self.supported_parameters())
        data.update(new_data)
        self._data = data

    @property
    def description(self):
        return self.data[CUBA.DESCRIPTION]

    @description.setter
    def description(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'description')
            validation.validate_cuba_keyword(value, 'description')
        data = self.data
        data[CUBA.DESCRIPTION] = value
        self.data = data

    @property
    def name(self):
        return self.data[CUBA.NAME]

    @name.setter
    def name(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'name')
            validation.validate_cuba_keyword(value, 'name')
        data = self.data
        data[CUBA.NAME] = value
        self.data = data

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
