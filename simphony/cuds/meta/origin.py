import uuid
from simphony.core.data_container import create_data_container
from simphony.core.cuba import CUBA
from .cuds_component import CUDSComponent
from . import validation

_RestrictedDataContainer = create_data_container(
    (CUBA.DESCRIPTION, CUBA.POINT, CUBA.UUID, CUBA.NAME),
    class_name="_RestrictedDataContainer")


class Origin(CUDSComponent):

    '''The origin of a space system  # noqa
    '''

    cuba_key = CUBA.ORIGIN

    def __init__(self, description=None, name=None, data=None, point=[0, 0, 0]):

        self.description = description
        self.name = name
        if data:
            self.data = data
        self.point = point
        # This is a system-managed, read-only attribute
        self._definition = 'The origin of a space system'  # noqa

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = _RestrictedDataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, _RestrictedDataContainer):
                raise TypeError("data is not a RestrictedDataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, _RestrictedDataContainer):
            self._data = new_data
        else:
            self._data = _RestrictedDataContainer(new_data)

    @property
    def point(self):
        return self.data[CUBA.POINT]

    @point.setter
    def point(self, value):
        value = validation.cast_data_type(value, 'point')
        validation.validate_cuba_keyword(value, 'point')
        self.data[CUBA.POINT] = value

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
        return (CUBA.DESCRIPTION, CUBA.POINT, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
