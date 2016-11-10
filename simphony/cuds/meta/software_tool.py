import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem
from . import validation


class SoftwareTool(CUDSItem):
    '''Represents a software tool which is used to solve the model or in pre/post processing  # noqa
    '''

    cuba_key = CUBA.SOFTWARE_TOOL

    def __init__(self, data=None, version=None):

        self._data = DataContainer()

        self.version = version
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
        return (CUBA.VERSION, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_ITEM, )
