import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_component import CUDSComponent
from . import validation


class PrimitiveCell(CUDSComponent):
    '''A lattice primitive cell  # noqa
    '''

    cuba_key = CUBA.PRIMITIVE_CELL

    def __init__(self,
                 data=None,
                 description="",
                 name="",
                 lattice_vectors=None):

        self._data = DataContainer()

        if lattice_vectors is None:
            self.lattice_vectors = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
                                    [0.0, 0.0, 1.0]]
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._definition = 'A lattice primitive cell'  # noqa

    @property
    def lattice_vectors(self):
        return self.data[CUBA.LATTICE_VECTORS]

    @lattice_vectors.setter
    def lattice_vectors(self, value):
        value = validation.cast_data_type(value, 'lattice_vectors')
        validation.validate_cuba_keyword(value, 'lattice_vectors')
        data = self.data
        data[CUBA.LATTICE_VECTORS] = value
        self.data = data

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
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.DESCRIPTION, CUBA.LATTICE_VECTORS, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
