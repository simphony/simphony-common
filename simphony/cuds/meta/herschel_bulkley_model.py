from simphony.core import Default  # noqa
from . import validation
from simphony.core.cuba import CUBA
from .rheology_model import RheologyModel


class HerschelBulkleyModel(RheologyModel):
    """
    Herschel-Bulkley model combines the effects of Bingham
    plastic and power-law behavior in a fluid
    """
    cuba_key = CUBA.HERSCHEL_BULKLEY_MODEL

    def __init__(self,
                 initial_viscosity=Default,
                 linear_constant=Default,
                 power_law_index=Default,
                 relaxation_time=Default,
                 description=Default,
                 name=Default):
        super(HerschelBulkleyModel, self).__init__(
            description=description, name=name)
        self._init_initial_viscosity(initial_viscosity)
        self._init_relaxation_time(relaxation_time)
        self._init_linear_constant(linear_constant)
        self._init_power_law_index(power_law_index)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(HerschelBulkleyModel,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(
            set((CUBA.INITIAL_VISCOSITY, CUBA.RELAXATION_TIME,
                 CUBA.LINEAR_CONSTANT, CUBA.POWER_LAW_INDEX, ) + base_params))

    def _default_definition(self):
        return "Herschel-Bulkley model combines the effects of Bingham plastic and power-law behavior in a fluid"  # noqa

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
        value = validation.cast_data_type(value, 'INITIAL_VISCOSITY')
        validation.check_valid_shape(value, [1], 'INITIAL_VISCOSITY')
        validation.validate_cuba_keyword(value, 'INITIAL_VISCOSITY')
        return value

    def _default_initial_viscosity(self):
        return 0.001

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _init_relaxation_time(self, value):
        if value is Default:
            value = self._default_relaxation_time()

        self.relaxation_time = value

    @property
    def relaxation_time(self):
        return self.data[CUBA.RELAXATION_TIME]

    @relaxation_time.setter
    def relaxation_time(self, value):
        value = self._validate_relaxation_time(value)
        self.data[CUBA.RELAXATION_TIME] = value

    def _validate_relaxation_time(self, value):
        value = validation.cast_data_type(value, 'RELAXATION_TIME')
        validation.check_valid_shape(value, [1], 'RELAXATION_TIME')
        validation.validate_cuba_keyword(value, 'RELAXATION_TIME')
        return value

    def _default_relaxation_time(self):
        return 1.0

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
        value = validation.cast_data_type(value, 'POWER_LAW_INDEX')
        validation.check_valid_shape(value, [1], 'POWER_LAW_INDEX')
        validation.validate_cuba_keyword(value, 'POWER_LAW_INDEX')
        return value

    def _default_power_law_index(self):
        return 1.0
