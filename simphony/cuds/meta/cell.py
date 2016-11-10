import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .mesh_element import MeshElement


class Cell(MeshElement):
    '''Element for storing 3D geometrical objects  # noqa
    '''

    cuba_key = CUBA.CELL

    def __init__(self, point):

        self._data = DataContainer()

        self.point = point
        # This is a system-managed, read-only attribute
        self._definition = 'Element for storing 3D geometrical objects'  # noqa

    @property
    def definition(self):
        return self._definition

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
        return (CUBA.UUID, CUBA.POINT)

    @classmethod
    def parents(cls):
        return (CUBA.MESH_ELEMENT, CUBA.CUDS_ITEM)
