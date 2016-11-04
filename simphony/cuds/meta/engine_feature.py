import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem


class EngineFeature(CUDSItem):
    '''Provides a physics equation and methods that engines provides to solve them  # noqa
    '''

    cuba_key = CUBA.ENGINE_FEATURE

    def __init__(self):

        self._data = DataContainer()

        # This is a system-managed, read-only attribute
        self._physics_equation = None
        # This is a system-managed, read-only attribute
        self._definition = 'Provides a physics equation and methods that engines provides to solve them'  # noqa
        # This is a system-managed, read-only attribute
        self._computational_method = None

    @property
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    @property
    def physics_equation(self):
        return self.data[CUBA.PHYSICS_EQUATION]

    @property
    def definition(self):
        return self._definition

    @property
    def computational_method(self):
        return self.data[CUBA.COMPUTATIONAL_METHOD]

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.PHYSICS_EQUATION, CUBA.UUID, CUBA.COMPUTATIONAL_METHOD)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_ITEM, )
