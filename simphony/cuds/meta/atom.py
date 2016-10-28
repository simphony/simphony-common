import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .particle import Particle
from . import validation


class Atom(Particle):
    '''An atom  # noqa
    '''

    cuba_key = CUBA.ATOM

    def __init__(self, position=None, data=None, mass=1.0):

        if position is None:
            self.position = [0, 0, 0]
        if data:
            self.data = data
        self.mass = mass
        # This is a system-managed, read-only attribute
        self._definition = 'An atom'  # noqa

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, DataContainer):
                raise TypeError("data is not a DataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, DataContainer):
            self._data = new_data
        else:
            self._data = DataContainer(new_data)

    @property
    def mass(self):
        return self.data[CUBA.MASS]

    @mass.setter
    def mass(self, value):
        value = validation.cast_data_type(value, 'mass')
        validation.validate_cuba_keyword(value, 'mass')
        self.data[CUBA.MASS] = value

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
        return (CUBA.POSITION, CUBA.MASS, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.PARTICLE, CUBA.POINT, CUBA.CUDS_ITEM)
