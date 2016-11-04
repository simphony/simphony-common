import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .point import Point


class Particle(Point):
    '''A particle in a 3D space system  # noqa
    '''

    cuba_key = CUBA.PARTICLE

    def __init__(self, position=None):

        self._data = DataContainer()

        if position is None:
            self.position = [0, 0, 0]
        # This is a system-managed, read-only attribute
        self._definition = 'A particle in a 3D space system'  # noqa

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
        return (CUBA.UUID, CUBA.POSITION)

    @classmethod
    def parents(cls):
        return (CUBA.POINT, CUBA.CUDS_ITEM)
