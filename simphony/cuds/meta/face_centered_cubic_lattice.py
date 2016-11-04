import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .bravais_lattice import BravaisLattice


class FaceCenteredCubicLattice(BravaisLattice):
    '''A face centred cubic lattice  # noqa
    '''

    cuba_key = CUBA.FACE_CENTERED_CUBIC_LATTICE

    def __init__(self,
                 primitive_cell,
                 description="",
                 name="",
                 lattice_parameter=None):

        self._data = DataContainer()

        self.primitive_cell = primitive_cell
        if lattice_parameter is None:
            self.lattice_parameter = [1.0, 1.0, 1.0]
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._definition = 'A face centred cubic lattice'  # noqa
        # This is a system-managed, read-only attribute
        self._origin = None
        # This is a system-managed, read-only attribute
        self._size = [1, 1, 1]

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
        return (CUBA.ORIGIN, CUBA.LATTICE_PARAMETER, CUBA.DESCRIPTION,
                CUBA.UUID, CUBA.PRIMITIVE_CELL, CUBA.SIZE, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.BRAVAIS_LATTICE, CUBA.LATTICE, CUBA.CUDS_COMPONENT,
                CUBA.CUDS_ITEM)
