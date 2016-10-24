import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem
from . import validation


class SoftwareTool(CUDSItem):
    '''Represents a software tool which is used to solve the model or in pre/post processing  # noqa
    '''

    cuba_key = CUBA.SOFTWARE_TOOL

    def __init__(self, version=None, data=None):

        self.version = version
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._definition = 'Represents a software tool which is used to solve the model or in pre/post processing'  # noqa

    @property
    def version(self):
        return self.data[CUBA.VERSION]

    @version.setter
    def version(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'version')
            validation.validate_cuba_keyword(value, 'version')
        data = self.data
        data[CUBA.VERSION] = value
        self.data = data

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer.new_with_restricted_keys(
                self.supported_parameters())
            data_container = self._data

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
    def definition(self):
        return self._definition

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.VERSION, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_ITEM, )
