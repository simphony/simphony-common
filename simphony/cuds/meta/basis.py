from . import validation
from simphony.core import Default
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class Basis(CUDSComponent):
    """
    Space basis vectors (row wise)
    """
    cuba_key = CUBA.BASIS

    def __init__(self, vector=Default, *args, **kwargs):
        super(Basis, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_vector(vector)

    def supported_parameters(self):
        try:
            base_params = super(Basis, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.VECTOR, ) + base_params

    def _init_definition(self):
        self._definition = "Space basis vectors (row wise)"  # noqa

    @property
    def definition(self):
        return self._definition

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
