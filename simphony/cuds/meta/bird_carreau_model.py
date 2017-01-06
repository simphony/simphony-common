from .rheology_model import RheologyModel
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class BirdCarreauModel(RheologyModel):
    """
    Bird-Carreau model
    """
    cuba_key = CUBA.BIRD_CARREAU_MODEL

    def __init__(self,
                 initial_viscosity=Default,
                 linear_constant=Default,
                 maximum_viscosity=Default,
                 power_law_index=Default,
                 *args,
                 **kwargs):
        super(BirdCarreauModel, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_initial_viscosity(initial_viscosity)
        self._init_models()
        self._init_linear_constant(linear_constant)
        self._init_maximum_viscosity(maximum_viscosity)
        self._init_power_law_index(power_law_index)

    def supported_parameters(self):
        try:
            base_params = super(BirdCarreauModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.INITIAL_VISCOSITY,
            CUBA.LINEAR_CONSTANT,
            CUBA.MAXIMUM_VISCOSITY,
            CUBA.POWER_LAW_INDEX, ) + base_params

    def _init_definition(self):
        self._definition = "Bird-Carreau model"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_initial_viscosity(self, value):
        if value is Default:
            value = 0.001

        self.initial_viscosity = value

    @property
    def initial_viscosity(self):
        return self.data[CUBA.INITIAL_VISCOSITY]

    @initial_viscosity.setter
    def initial_viscosity(self, value):
        value = self._validate_initial_viscosity(value)
        self.data[CUBA.INITIAL_VISCOSITY] = value

    def _validate_initial_viscosity(self, value):
        value = validation.cast_data_type(value, 'CUBA.INITIAL_VISCOSITY')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'CUBA.INITIAL_VISCOSITY')
        return value

    def _init_models(self):
        self._models = ['CUBA.CONTINUUM']  # noqa

    @property
    def models(self):
        return self._models

    def _init_linear_constant(self, value):
        if value is Default:
            value = 1.0

        self.linear_constant = value

    @property
    def linear_constant(self):
        return self.data[CUBA.LINEAR_CONSTANT]

    @linear_constant.setter
    def linear_constant(self, value):
        value = self._validate_linear_constant(value)
        self.data[CUBA.LINEAR_CONSTANT] = value

    def _validate_linear_constant(self, value):
        value = validation.cast_data_type(value, 'CUBA.LINEAR_CONSTANT')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'CUBA.LINEAR_CONSTANT')
        return value

    def _init_maximum_viscosity(self, value):
        if value is Default:
            value = 1e-05

        self.maximum_viscosity = value

    @property
    def maximum_viscosity(self):
        return self.data[CUBA.MAXIMUM_VISCOSITY]

    @maximum_viscosity.setter
    def maximum_viscosity(self, value):
        value = self._validate_maximum_viscosity(value)
        self.data[CUBA.MAXIMUM_VISCOSITY] = value

    def _validate_maximum_viscosity(self, value):
        value = validation.cast_data_type(value, 'CUBA.MAXIMUM_VISCOSITY')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'CUBA.MAXIMUM_VISCOSITY')
        return value

    def _init_power_law_index(self, value):
        if value is Default:
            value = 0.5

        self.power_law_index = value

    @property
    def power_law_index(self):
        return self.data[CUBA.POWER_LAW_INDEX]

    @power_law_index.setter
    def power_law_index(self, value):
        value = self._validate_power_law_index(value)
        self.data[CUBA.POWER_LAW_INDEX] = value

    def _validate_power_law_index(self, value):
        value = validation.cast_data_type(value, 'CUBA.POWER_LAW_INDEX')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'CUBA.POWER_LAW_INDEX')
        return value
