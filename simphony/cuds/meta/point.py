import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem
from . import validation


class Point(CUDSItem):
    '''A point in a 3D space system  # noqa
    '''

    cuba_key = CUBA.POINT

    def __init__(self, data=None, position=None):

        if position is None:
            self.position = [0, 0, 0]
        if data:
            internal_data = self.data
            internal_data.update(data)
            self.data = internal_data

        # This is a system-managed, read-only attribute
        self._definition = 'A point in a 3D space system'  # noqa

    @property
    def position(self):
        return self.data[CUBA.POSITION]

    @position.setter
    def position(self, value):
        value = validation.cast_data_type(value, 'position')
        validation.validate_cuba_keyword(value, 'position')
        data = self.data
        data[CUBA.POSITION] = value
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
        return (CUBA.POSITION, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_ITEM, )
