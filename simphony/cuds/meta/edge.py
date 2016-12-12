import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .mesh_element import MeshElement


class Edge(MeshElement):
    '''Element for storing 1D geometrical objects  # noqa
    '''

    cuba_key = CUBA.EDGE

    def __init__(self, point):

        self._data = DataContainer()

        self.point = point
        # This is a system-managed, read-only attribute
        self._definition = 'Element for storing 1D geometrical objects'  # noqa

    @property
    def definition(self):
        return self._definition

    @property
    def data(self):
        return self._data

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
        return (CUBA.POINT, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.MESH_ELEMENT, CUBA.CUDS_ITEM)
