from simphony.core import Default  # noqa
from .condition import Condition
from simphony.core.cuba import CUBA
from simphony.cuds import meta_validation


class SlipVelocity(Condition):
    """
    Wall free slip velocity boundary condition
    """
    cuba_key = CUBA.SLIP_VELOCITY

    def __init__(self, variable=Default, description=Default, name=Default):
        super(SlipVelocity, self).__init__(description=description, name=name)
        self._init_models()
        self._init_variable(variable)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(SlipVelocity, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.VARIABLE, ) + base_params))

    def _init_models(self):
        self._models = self._default_models()  # noqa

    @property
    def models(self):
        return self._models

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Wall free slip velocity boundary condition"  # noqa

    def _init_variable(self, value):
        if value is Default:
            value = self._default_variable()

        self.variable = value

    @property
    def variable(self):
        return self.data[CUBA.VARIABLE]

    @variable.setter
    def variable(self, value):
        value = self._validate_variable(value)
        self.data[CUBA.VARIABLE] = value

    def _validate_variable(self, value):
        value = meta_validation.cast_data_type(value, 'VARIABLE')
        meta_validation.check_valid_shape(value, [None], 'VARIABLE')
        meta_validation.check_elements(value, [None], 'VARIABLE')

        return value

    def _default_variable(self):
        return []
