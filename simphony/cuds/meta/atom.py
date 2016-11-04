import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .particle import Particle
from . import validation


class Atom(Particle):
    '''An atom  # noqa
    '''

    cuba_key = CUBA.ATOM

    def __init__(self, position=None, mass=1.0):

        self._data = DataContainer()

        self.mass = mass
        if position is None:
            self.position = [0, 0, 0]
        # This is a system-managed, read-only attribute
        self._definition = 'An atom'  # noqa

    @property
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

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
    def definition(self):
        return self._definition

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.MASS, CUBA.UUID, CUBA.POSITION)

    @classmethod
    def parents(cls):
        return (CUBA.PARTICLE, CUBA.POINT, CUBA.CUDS_ITEM)
