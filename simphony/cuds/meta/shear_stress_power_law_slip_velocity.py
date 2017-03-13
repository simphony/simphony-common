from simphony.core import Default  # noqa
from . import validation
from .condition import Condition
from simphony.core.cuba import CUBA


class ShearStressPowerLawSlipVelocity(Condition):
    """
    Shear stress power law dependant slip velocity boundary
    condition. Nonlinear boundary condition for wall tangential
    velocity of the form v_s = CUBA.LINEAR_CONSTANT *
    S^CUBA.POWER_LAW_INDEX where v_s is the slip velocity
    (tangential velocity on the wall) and S is the wall shear
    stress
    """
    cuba_key = CUBA.SHEAR_STRESS_POWER_LAW_SLIP_VELOCITY

    def __init__(self,
                 density=Default,
                 linear_constant=Default,
                 power_law_index=Default,
                 variable=Default,
                 description=Default,
                 name=Default):
        super(ShearStressPowerLawSlipVelocity, self).__init__(
            description=description, name=name)
        self._init_density(density)
        self._init_models()
        self._init_variable(variable)
        self._init_linear_constant(linear_constant)
        self._init_power_law_index(power_law_index)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(ShearStressPowerLawSlipVelocity,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(
            set((
                CUBA.DENSITY,
                CUBA.VARIABLE,
                CUBA.LINEAR_CONSTANT,
                CUBA.POWER_LAW_INDEX, ) + base_params))

    def _default_definition(self):
        return "Shear stress power law dependant slip velocity boundary condition. Nonlinear boundary condition for wall tangential velocity of the form v_s = CUBA.LINEAR_CONSTANT * S^CUBA.POWER_LAW_INDEX where v_s is the slip velocity (tangential velocity on the wall) and S is the wall shear stress"  # noqa

    def _init_density(self, value):
        if value is Default:
            value = self._default_density()

        self.density = value

    @property
    def density(self):
        return self.data[CUBA.DENSITY]

    @density.setter
    def density(self, value):
        value = self._validate_density(value)
        self.data[CUBA.DENSITY] = value

    def _validate_density(self, value):
        value = validation.cast_data_type(value, 'DENSITY')
        validation.check_valid_shape(value, [1], 'DENSITY')
        validation.validate_cuba_keyword(value, 'DENSITY')
        return value

    def _default_density(self):
        return 1000.0

    def _init_models(self):
        self._models = self._default_models()  # noqa

    @property
    def models(self):
        return self._models

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

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
        value = validation.cast_data_type(value, 'VARIABLE')
        validation.check_valid_shape(value, [None], 'VARIABLE')
        validation.check_elements(value, [None], 'VARIABLE')

        return value

    def _default_variable(self):
        return []

    def _init_linear_constant(self, value):
        if value is Default:
            value = self._default_linear_constant()

        self.linear_constant = value

    @property
    def linear_constant(self):
        return self.data[CUBA.LINEAR_CONSTANT]

    @linear_constant.setter
    def linear_constant(self, value):
        value = self._validate_linear_constant(value)
        self.data[CUBA.LINEAR_CONSTANT] = value

    def _validate_linear_constant(self, value):
        value = validation.cast_data_type(value, 'LINEAR_CONSTANT')
        validation.check_valid_shape(value, [1], 'LINEAR_CONSTANT')
        validation.validate_cuba_keyword(value, 'LINEAR_CONSTANT')
        return value

    def _default_linear_constant(self):
        return 1.0

    def _init_power_law_index(self, value):
        if value is Default:
            value = self._default_power_law_index()

        self.power_law_index = value

    @property
    def power_law_index(self):
        return self.data[CUBA.POWER_LAW_INDEX]

    @power_law_index.setter
    def power_law_index(self, value):
        value = self._validate_power_law_index(value)
        self.data[CUBA.POWER_LAW_INDEX] = value

    def _validate_power_law_index(self, value):
        value = validation.cast_data_type(value, 'POWER_LAW_INDEX')
        validation.check_valid_shape(value, [1], 'POWER_LAW_INDEX')
        validation.validate_cuba_keyword(value, 'POWER_LAW_INDEX')
        return value

    def _default_power_law_index(self):
        return 1.0
