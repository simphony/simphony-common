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
                 description=None,
                 name=None,
                 data=None,
                 lattice_vectors=None):

        self.description = description
        self.name = name
        if data:
            self.data = data
        if lattice_vectors is None:
            self.lattice_vectors = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
                                    [0.0, 0.0, 1.0]]
        # This is a system-managed, read-only attribute
        self._definition = 'A lattice primitive cell'  # noqa

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
    def lattice_vectors(self):
        return self.data[CUBA.LATTICE_VECTORS]

    @lattice_vectors.setter
    def lattice_vectors(self, value):
        value = validation.cast_data_type(value, 'lattice_vectors')
        validation.validate_cuba_keyword(value, 'lattice_vectors')
        self.data[CUBA.LATTICE_VECTORS] = value

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
