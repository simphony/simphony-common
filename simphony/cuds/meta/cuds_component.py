import uuid
from simphony.core import data_container as dc
from simphony.core import cuba as cb
from .cuds_item import CUDSItem
from . import validation


class CUDSComponent(CUDSItem):

    '''Base data type for the CUDS components  # noqa
    '''

    cuba_key = cb.CUBA.CUDS_COMPONENT

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
    def description(self):
        return self.data[cb.CUBA.DESCRIPTION]

    @description.setter
    def description(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'description')
            validation.validate_cuba_keyword(value, 'description')
        self.data[cb.CUBA.DESCRIPTION] = value

    @property
    def name(self):
        return self.data[cb.CUBA.NAME]

    @name.setter
    def name(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'name')
            validation.validate_cuba_keyword(value, 'name')
        self.data[cb.CUBA.NAME] = value

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
        return (cb.CUBA.UUID, cb.CUBA.DESCRIPTION, cb.CUBA.NAME)

    @classmethod
    def parents(cls):
        return (cb.CUBA.CUDS_ITEM,)
