import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .boundary import Boundary
from . import validation


class Box(Boundary):
    '''A simple hexahedron (with six faces) simulation box defined by the three vectors and three directions. The condition should be specified for each direction (two faces at a time).  # noqa
    '''

    cuba_key = CUBA.BOX

    def __init__(self,
                 description=None,
                 name=None,
                 data=None,
                 condition=None,
                 vector=None):

        self.description = description
        self.name = name
        if data:
            self.data = data
        self.condition = condition
        if vector is None:
            self.vector = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        # This is a system-managed, read-only attribute
        self._definition = 'A simple hexahedron (with six faces) simulation box defined by the three vectors and three directions. The condition should be specified for each direction (two faces at a time).'  # noqa

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
    def condition(self):
        return self.data[CUBA.CONDITION]

    @condition.setter
    def condition(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'condition')
            validation.check_shape(value, '(3)')
            for item in value:
                validation.validate_cuba_keyword(item, 'condition')
        self.data[CUBA.CONDITION] = value

    @property
    def vector(self):
        return self.data[CUBA.VECTOR]

    @vector.setter
    def vector(self, value):
        value = validation.cast_data_type(value, 'vector')
        validation.check_shape(value, '(3,3)')
        for item in value:
            validation.validate_cuba_keyword(item, 'vector')
        self.data[CUBA.VECTOR] = value

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
        return (CUBA.VECTOR, CUBA.DESCRIPTION, CUBA.UUID, CUBA.CONDITION,
                CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.BOUNDARY, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
