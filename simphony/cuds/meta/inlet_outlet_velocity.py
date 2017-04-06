from simphony.core import Default  # noqa
from .mixed_condition import MixedCondition
from simphony.core.cuba import CUBA
from simphony.cuds import meta_validation


class InletOutletVelocity(MixedCondition):
    """
    Inlet outlet boundary condition (outlet condition is zero
    gradient and inlet given variable value)
    """
    cuba_key = CUBA.INLET_OUTLET_VELOCITY

    def __init__(self, velocity, material, description=Default, name=Default):
        super(InletOutletVelocity, self).__init__(
            material=material, description=description, name=name)
        self._init_models()
        self._init_variables()
        self._init_velocity(velocity)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(InletOutletVelocity,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.VELOCITY, ) + base_params))

    def _init_models(self):
        self._models = self._default_models()  # noqa

    @property
    def models(self):
        return self._models

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Inlet outlet boundary condition (outlet condition is zero gradient and inlet given variable value)"  # noqa

    def _init_variables(self):
        self._variables = self._default_variables()  # noqa

    @property
    def variables(self):
        return self._variables

    def _default_variables(self):
        return ['CUBA.VELOCITY']  # noqa

    def _init_velocity(self, value):
        if value is Default:
            value = self._default_velocity()

        self.velocity = value

    @property
    def velocity(self):
        return self.data[CUBA.VELOCITY]

    @velocity.setter
    def velocity(self, value):
        value = self._validate_velocity(value)
        self.data[CUBA.VELOCITY] = value

    def _validate_velocity(self, value):
        value = meta_validation.cast_data_type(value, 'VELOCITY')
        meta_validation.check_valid_shape(value, [1], 'VELOCITY')
        meta_validation.validate_cuba_keyword(value, 'VELOCITY')
        return value

    def _default_velocity(self):
        raise TypeError("No default for velocity")
