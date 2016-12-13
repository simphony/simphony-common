import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .bravais_lattice import BravaisLattice


class HexagonalLattice(BravaisLattice):
    '''A hexagonal lattice  # noqa
    '''

    cuba_key = CUBA.HEXAGONAL_LATTICE

    def __init__(self,
                 primitive_cell,
                 origin,
                 description="",
                 name="",
                 lattice_parameter=None,
                 size=None):

        self._data = DataContainer()

        self.origin = origin
        self.primitive_cell = primitive_cell
        if size is None:
            self.size = [1, 1, 1]
        if lattice_parameter is None:
            self.lattice_parameter = [1.0, 1.0, 1.0]
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._definition = 'A hexagonal lattice'  # noqa
        # This is a system-managed, read-only attribute
        self._models = []

    @property
    def definition(self):
        return self._definition

    @property
    def models(self):
        return self._models

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
        return (CUBA.DESCRIPTION, CUBA.LATTICE_PARAMETER, CUBA.NAME,
                CUBA.ORIGIN, CUBA.PRIMITIVE_CELL, CUBA.SIZE, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.BRAVAIS_LATTICE, CUBA.LATTICE, CUBA.DATA_SET,
                CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
