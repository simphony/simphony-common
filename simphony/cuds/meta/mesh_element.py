import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem
from . import validation


class MeshElement(CUDSItem):
    '''An element for storing geometrical objects  # noqa
    '''

    cuba_key = CUBA.MESH_ELEMENT

    def __init__(self, point):

        self._data = DataContainer()

        self.point = point
        # This is a system-managed, read-only attribute
        self._definition = 'An element for storing geometrical objects'  # noqa

    @property
    def point(self):
        return self.data[CUBA.POINT]

    @point.setter
    def point(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'point')
            validation.check_shape(value, '(:)')
            for item in value:
                validation.validate_cuba_keyword(item, 'point')
        data = self.data
        data[CUBA.POINT] = value
        self.data = data

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
        return (CUBA.CUDS_ITEM, )
