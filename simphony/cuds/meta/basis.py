from simphony.core import Default  # noqa
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA
from simphony.cuds import meta_validation


class Basis(CUDSComponent):
    """
    Space basis vectors (row wise)
    """
    cuba_key = CUBA.BASIS

    def __init__(self, vector=Default, description=Default, name=Default):
        super(Basis, self).__init__(description=description, name=name)
        self._init_vector(vector)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Basis, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.VECTOR, ) + base_params))

    def _default_definition(self):
        return "Space basis vectors (row wise)"  # noqa

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
        value = meta_validation.cast_data_type(value, 'VECTOR')
        meta_validation.check_valid_shape(value, [3], 'VECTOR')
        meta_validation.check_elements(value, [3], 'VECTOR')

        return value

    def _default_vector(self):
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
