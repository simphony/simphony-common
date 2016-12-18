import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .data_set import DataSet
from . import validation


class Particles(DataSet):
    '''A collection of particles  # noqa
    '''

    cuba_key = CUBA.PARTICLES

    def __init__(self, particle, bond, description="", name=""):

        self._data = DataContainer()

        self.bond = bond
        self.particle = particle
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._definition = 'A collection of particles'  # noqa
        # This is a system-managed, read-only attribute
        self._models = []

    @property
    def bond(self):
        return self.data[CUBA.BOND]

    @bond.setter
    def bond(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'bond')
            validation.check_shape(value, '(:)')
            for item in value:
                validation.validate_cuba_keyword(item, 'bond')
        data = self.data
        data[CUBA.BOND] = value
        self.data = data

    @property
    def particle(self):
        return self.data[CUBA.PARTICLE]

    @particle.setter
    def particle(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'particle')
            validation.check_shape(value, '(:)')
            for item in value:
                validation.validate_cuba_keyword(item, 'particle')
        data = self.data
        data[CUBA.PARTICLE] = value
        self.data = data

    @property
    def definition(self):
        return self._definition

    @property
    def models(self):
        return self._models

    @property
    def data(self):
        return self._data

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
        return (CUBA.BOND, CUBA.DESCRIPTION, CUBA.NAME, CUBA.PARTICLE,
                CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.DATA_SET, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
