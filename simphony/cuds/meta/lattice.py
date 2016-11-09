import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_component import CUDSComponent


class Lattice(CUDSComponent):
    '''A lattice  # noqa
    '''

    cuba_key = CUBA.LATTICE

    def __init__(self, data=None, description=None, name=None):

        self.name = name
        self.description = description
        if data:
            internal_data = self.data
            internal_data.update(data)
            self.data = internal_data

        # This is a system-managed, read-only attribute
        self._origin = None
        # This is a system-managed, read-only attribute
        self._definition = 'A lattice'  # noqa
        # This is a system-managed, read-only attribute
        self._size = None
        # This is a system-managed, read-only attribute
        self._primitive_cell = None

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
    def origin(self):
        return self._origin

    @property
    def definition(self):
        return self._definition

    @property
    def size(self):
        return self._size

    @property
    def primitive_cell(self):
        return self._primitive_cell

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.ORIGIN, CUBA.DESCRIPTION, CUBA.PRIMITIVE_CELL, CUBA.SIZE,
                CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
