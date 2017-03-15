from simphony.core import Default  # noqa
from simphony.cuds import meta_validation
from simphony.core.cuba import CUBA
from .rheology_model import RheologyModel


class CrossPowerLawModel(RheologyModel):
    """
    Viscosity Cross power law model
    """
    cuba_key = CUBA.CROSS_POWER_LAW_MODEL

    def __init__(self,
                 initial_viscosity=Default,
                 linear_constant=Default,
                 maximum_viscosity=Default,
                 power_law_index=Default,
                 description=Default,
                 name=Default):
        super(CrossPowerLawModel, self).__init__(
            description=description, name=name)
        self._init_initial_viscosity(initial_viscosity)
        self._init_linear_constant(linear_constant)
        self._init_maximum_viscosity(maximum_viscosity)
        self._init_power_law_index(power_law_index)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(CrossPowerLawModel, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(
            set((
                CUBA.INITIAL_VISCOSITY,
                CUBA.LINEAR_CONSTANT,
                CUBA.MAXIMUM_VISCOSITY,
                CUBA.POWER_LAW_INDEX, ) + base_params))

    def _default_definition(self):
        return "Viscosity Cross power law model"  # noqa

    def _init_initial_viscosity(self, value):
        if value is Default:
            value = self._default_initial_viscosity()

        self.initial_viscosity = value

    @property
    def initial_viscosity(self):
        return self.data[CUBA.INITIAL_VISCOSITY]

    @initial_viscosity.setter
    def initial_viscosity(self, value):
        value = self._validate_initial_viscosity(value)
        self.data[CUBA.INITIAL_VISCOSITY] = value

    def _validate_initial_viscosity(self, value):
        value = meta_validation.cast_data_type(value, 'INITIAL_VISCOSITY')
        meta_validation.check_valid_shape(value, [1], 'INITIAL_VISCOSITY')
        meta_validation.validate_cuba_keyword(value, 'INITIAL_VISCOSITY')
        return value

    def _default_initial_viscosity(self):
        return 0.001

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

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
        value = meta_validation.cast_data_type(value, 'LINEAR_CONSTANT')
        meta_validation.check_valid_shape(value, [1], 'LINEAR_CONSTANT')
        meta_validation.validate_cuba_keyword(value, 'LINEAR_CONSTANT')
        return value

    def _default_linear_constant(self):
        return 1.0

    def _init_maximum_viscosity(self, value):
        if value is Default:
            value = self._default_maximum_viscosity()

        self.maximum_viscosity = value

    @property
    def maximum_viscosity(self):
        return self.data[CUBA.MAXIMUM_VISCOSITY]

    @maximum_viscosity.setter
    def maximum_viscosity(self, value):
        value = self._validate_maximum_viscosity(value)
        self.data[CUBA.MAXIMUM_VISCOSITY] = value

    def _validate_maximum_viscosity(self, value):
        value = meta_validation.cast_data_type(value, 'MAXIMUM_VISCOSITY')
        meta_validation.check_valid_shape(value, [1], 'MAXIMUM_VISCOSITY')
        meta_validation.validate_cuba_keyword(value, 'MAXIMUM_VISCOSITY')
        return value

    def _default_maximum_viscosity(self):
        return 1e-05

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
        value = meta_validation.cast_data_type(value, 'POWER_LAW_INDEX')
        meta_validation.check_valid_shape(value, [1], 'POWER_LAW_INDEX')
        meta_validation.validate_cuba_keyword(value, 'POWER_LAW_INDEX')
        return value

    def _default_power_law_index(self):
        return 0.5
