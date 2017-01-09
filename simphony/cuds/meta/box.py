from . import validation
from simphony.core import Default
from .boundary import Boundary
from simphony.core.cuba import CUBA


class Box(Boundary):
    """
    A simple hexahedron simulation box defining six boundary
    faces that are defined by three box vectors. The same
    boundary condition should be specified for each direction
    (two faces at a time).
    """
    cuba_key = CUBA.BOX

    def __init__(self,
                 vector,
                 condition=Default,
                 description=Default,
                 name=Default):

        super(Box, self).__init__(
            condition=condition, description=description, name=name)
        self._init_vector(vector)

    def supported_parameters(self):
        try:
            base_params = super(Box, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.CONDITION,
            CUBA.VECTOR, ) + base_params

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
        validation.check_shape(value, [3])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if hasattr(value, "flatten"):
            flat_array = value.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'CONDITION')

        return value

    def _default_condition(self):
        return None

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
        validation.check_shape(value, [3])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if hasattr(value, "flatten"):
            flat_array = value.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'VECTOR')

        return value

    def _default_vector(self):
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
