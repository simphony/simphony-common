from . import validation
from simphony.core import Default
from .boundary import Boundary
from simphony.core.cuba import CUBA


class Box(Boundary):
    """
    A simple hexahedron simulation box defining six boundary faces that are defined by three box vectors. The same boundary condition should be specified for each direction (two faces at a time).
    """

    cuba_key = CUBA.BOX

    def __init__(self, condition=Default, vector=Default, *args, **kwargs):
        super(Box, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_condition(condition)
        self._init_vector(vector)

    def supported_parameters(self):
        try:
            base_params = super(Box, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.CONDITION,
            CUBA.VECTOR, ) + base_params

    def _init_definition(self):
        self._definition = "A simple hexahedron simulation box defining six boundary faces that are defined by three box vectors. The same boundary condition should be specified for each direction (two faces at a time)."

    @property
    def definition(self):
        return self._definition

    def _init_condition(self, value):
        if value is Default:
            value = None

        self.condition = value

    @property
    def condition(self):
        return self.data[CUBA.CONDITION]

    @condition.setter
    def condition(self, value):
        value = self._validate_condition(value)
        self.data[CUBA.CONDITION] = value

    def _validate_condition(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.CONDITION')
        validation.check_shape(value, [3])
        for tuple_ in itertools.product(*[range(x) for x in [3]]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.CONDITION')

        return value

    def _init_vector(self, value):
        if value is Default:
            value = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        self.vector = value

    @property
    def vector(self):
        return self.data[CUBA.VECTOR]

    @vector.setter
    def vector(self, value):
        value = self._validate_vector(value)
        self.data[CUBA.VECTOR] = value

    def _validate_vector(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.VECTOR')
        validation.check_shape(value, [3])
        for tuple_ in itertools.product(*[range(x) for x in [3]]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.VECTOR')

        return value
