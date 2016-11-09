import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_component import CUDSComponent
from . import validation


class Origin(CUDSComponent):
    '''The origin of a space system  # noqa
    '''

    cuba_key = CUBA.ORIGIN

    def __init__(self, description="", name="", position=None):

        self._data = DataContainer()

        if position is None:
            self.position = [0, 0, 0]
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._definition = 'The origin of a space system'  # noqa

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
    def definition(self):
        return self._definition

    @property
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.DESCRIPTION, CUBA.POSITION, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
