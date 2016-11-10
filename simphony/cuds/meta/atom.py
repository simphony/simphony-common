import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .particle import Particle
from . import validation


class Atom(Particle):
    '''An atom  # noqa
    '''

    cuba_key = CUBA.ATOM

    def __init__(self, data=None, position=None, mass=1.0):

        self.mass = mass
        if position is None:
            self.position = [0, 0, 0]
        if data:
            internal_data = self.data
            internal_data.update(data)
            self.data = internal_data

        # This is a system-managed, read-only attribute
        self._definition = 'An atom'  # noqa

    @property
    def mass(self):
        return self.data[CUBA.MASS]

    @mass.setter
    def mass(self, value):
        value = validation.cast_data_type(value, 'mass')
        validation.validate_cuba_keyword(value, 'mass')
        data = self.data
        data[CUBA.MASS] = value
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
        return (CUBA.MASS, CUBA.POSITION, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.PARTICLE, CUBA.POINT, CUBA.CUDS_ITEM)
