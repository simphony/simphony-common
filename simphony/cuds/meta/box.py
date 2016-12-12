import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .boundary import Boundary
from . import validation


class Box(Boundary):
    '''A simple hexahedron (with six faces) simulation box defined by the three vectors and three directions. The condition should be specified for each direction (two faces at a time).  # noqa
    '''

    cuba_key = CUBA.BOX

    def __init__(self, description="", name="", condition=None, vector=None):

        self._data = DataContainer()

        if vector is None:
            self.vector = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.condition = condition
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._definition = 'A simple hexahedron (with six faces) simulation box defined by the three vectors and three directions. The condition should be specified for each direction (two faces at a time).'  # noqa

    @property
    def vector(self):
        return self.data[CUBA.VECTOR]

    @vector.setter
    def vector(self, value):
        value = validation.cast_data_type(value, 'vector')
        validation.check_shape(value, '(3,3)')
        for item in value:
            validation.validate_cuba_keyword(item, 'vector')
        data = self.data
        data[CUBA.VECTOR] = value
        self.data = data

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
        data = self.data
        data[CUBA.CONDITION] = value
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
        return (CUBA.CONDITION, CUBA.DESCRIPTION, CUBA.NAME, CUBA.UUID,
                CUBA.VECTOR)

    @classmethod
    def parents(cls):
        return (CUBA.BOUNDARY, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
