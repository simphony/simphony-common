import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .bravais_lattice import BravaisLattice


class BodyCenteredTetragonalLattice(BravaisLattice):
    '''A body centered tetragonal lattice  # noqa
    '''

    cuba_key = CUBA.BODY_CENTERED_TETRAGONAL_LATTICE

    def __init__(self,
                 primitive_cell=None,
                 lattice_parameter=None,
                 description=None,
                 name=None,
                 data=None):

        if primitive_cell is None:
            self.primitive_cell = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
                                   [0.0, 0.0, 1.0]]
        if lattice_parameter is None:
            self.lattice_parameter = [1.0, 1.0, 1.0]
        self.description = description
        self.name = name
        if data:
            self.data = data
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
