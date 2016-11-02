import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .mesh_element import MeshElement


class Cell(MeshElement):
    '''Element for storing 3D geometrical objects  # noqa
    '''

    cuba_key = CUBA.CELL

    def __init__(self, point, data=None):

        self.point = point
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._definition = 'Element for storing 3D geometrical objects'  # noqa

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
