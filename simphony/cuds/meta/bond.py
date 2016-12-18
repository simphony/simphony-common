import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem
from . import validation


class Bond(CUDSItem):
    '''A bond between two or more atoms or particles  # noqa
    '''

    cuba_key = CUBA.BOND

    def __init__(self, particle):

        self._data = DataContainer()

        self.particle = particle
        # This is a system-managed, read-only attribute
        self._definition = 'A bond between two or more atoms or particles'  # noqa

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
        return (CUBA.PARTICLE, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_ITEM, )
