import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .lattice import Lattice
from . import validation


class BravaisLattice(Lattice):
    '''A Bravais lattice  # noqa
    '''

    cuba_key = CUBA.BRAVAIS_LATTICE

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
        self._origin = None
        # This is a system-managed, read-only attribute
        self._definition = 'A Bravais lattice'  # noqa
        # This is a system-managed, read-only attribute
        self._size = [1, 1, 1]

    @property
    def primitive_cell(self):
        return self.data[CUBA.PRIMITIVE_CELL]

    @primitive_cell.setter
    def primitive_cell(self, value):
        value = validation.cast_data_type(value, 'primitive_cell')
        validation.validate_cuba_keyword(value, 'primitive_cell')
        data = self.data
        data[CUBA.PRIMITIVE_CELL] = value
        self.data = data

    @property
    def lattice_parameter(self):
        return self.data[CUBA.LATTICE_PARAMETER]

    @lattice_parameter.setter
    def lattice_parameter(self, value):
        value = validation.cast_data_type(value, 'lattice_parameter')
        validation.check_shape(value, '(3)')
        for item in value:
            validation.validate_cuba_keyword(item, 'lattice_parameter')
        data = self.data
        data[CUBA.LATTICE_PARAMETER] = value
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
    def origin(self):
        return self._origin

    @property
    def definition(self):
        return self._definition

    @property
    def size(self):
        return self._size

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.ORIGIN, CUBA.LATTICE_PARAMETER, CUBA.DESCRIPTION,
                CUBA.UUID, CUBA.PRIMITIVE_CELL, CUBA.SIZE, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.LATTICE, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
