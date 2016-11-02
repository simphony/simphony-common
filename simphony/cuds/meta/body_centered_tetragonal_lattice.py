import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .bravais_lattice import BravaisLattice


class BodyCenteredTetragonalLattice(BravaisLattice):
    '''A body centered tetragonal lattice  # noqa
    '''

    cuba_key = CUBA.BODY_CENTERED_TETRAGONAL_LATTICE

    def __init__(self,
                 primitive_cell,
                 data=None,
                 description=None,
                 name=None,
                 lattice_parameter=None):

        self.primitive_cell = primitive_cell
        if lattice_parameter is None:
            self.lattice_parameter = [1.0, 1.0, 1.0]
        self.name = name
        self.description = description
        if data:
            internal_data = self.data
            internal_data.update(data)
            self.data = internal_data

        # This is a system-managed, read-only attribute
        self._definition = 'A body centered tetragonal lattice'  # noqa
        # This is a system-managed, read-only attribute
        self._origin = None
        # This is a system-managed, read-only attribute
        self._size = [1, 1, 1]

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
    def origin(self):
        return self._origin

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @property
    def size(self):
        return self._size

    @classmethod
    def supported_parameters(cls):
        return (CUBA.PRIMITIVE_CELL, CUBA.LATTICE_PARAMETER, CUBA.DESCRIPTION,
                CUBA.SIZE, CUBA.UUID, CUBA.ORIGIN, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.BRAVAIS_LATTICE, CUBA.LATTICE, CUBA.CUDS_COMPONENT,
                CUBA.CUDS_ITEM)
