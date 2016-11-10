import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_component import CUDSComponent


class Particles(CUDSComponent):
    '''A collection of particles  # noqa
    '''

    cuba_key = CUBA.PARTICLES

    def __init__(self, data=None, description="", name=""):

        self._data = DataContainer()

        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._definition = 'A collection of particles'  # noqa
        # This is a system-managed, read-only attribute
        self._particle = None
        # This is a system-managed, read-only attribute
        self._bond = None

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
    def particle(self):
        return self._particle

    @property
    def bond(self):
        return self._bond

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.DESCRIPTION, CUBA.PARTICLE, CUBA.BOND, CUBA.UUID,
                CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
