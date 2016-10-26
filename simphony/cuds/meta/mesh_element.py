import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem
from . import validation


class MeshElement(CUDSItem):
    '''An element for storing geometrical objects  # noqa
    '''

    cuba_key = CUBA.MESH_ELEMENT

    def __init__(self, point, data=None):

        self.point = point
        if data:
            self.data = data
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
        self.data[CUBA.POINT] = value

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
        return (CUBA.CUDS_ITEM, )
