from simphony.core import Default  # noqa
from . import validation
from .boundary import Boundary
from simphony.core.cuba import CUBA
from .empty import Empty


class Box(Boundary):
    """
    A simple hexahedron simulation box defining six boundary
    faces that are defined by three box vectors. The same
    boundary condition should be specified for each direction
    (two faces at a time).
    """
    cuba_key = CUBA.BOX

    def __init__(self,
                 condition=Default,
                 vector=Default,
                 description=Default,
                 name=Default):
        super(Box, self).__init__(
            condition=condition, description=description, name=name)
        self._init_vector(vector)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Box, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.CONDITION, CUBA.VECTOR, ) + base_params))

    def _default_definition(self):
        return "A simple hexahedron simulation box defining six boundary faces that are defined by three box vectors. The same boundary condition should be specified for each direction (two faces at a time)."  # noqa

    def _init_condition(self, value):
        if value is Default:
            value = self._default_condition()

        self.condition = value

    @property
    def condition(self):
        return self.data[CUBA.CONDITION]

    @condition.setter
    def condition(self, value):
        value = self._validate_condition(value)
        self.data[CUBA.CONDITION] = value

    def _validate_condition(self, value):
        value = validation.cast_data_type(value, 'CONDITION')
        validation.check_valid_shape(value, [3], 'CONDITION')
        validation.check_elements(value, [3], 'CONDITION')

        return value

    def _default_condition(self):
        return [Empty(), Empty(), Empty()]

    def _init_vector(self, value):
        if value is Default:
            value = self._default_vector()

        self.vector = value

    @property
    def vector(self):
        return self.data[CUBA.VECTOR]

    @vector.setter
    def vector(self, value):
        value = self._validate_vector(value)
        self.data[CUBA.VECTOR] = value

    def _validate_vector(self, value):
        value = validation.cast_data_type(value, 'VECTOR')
        validation.check_valid_shape(value, [3], 'VECTOR')
        validation.check_elements(value, [3], 'VECTOR')

        return value

    def _default_vector(self):
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
