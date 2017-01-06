from .rheology_model import RheologyModel
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class HerschelBulkleyModel(RheologyModel):
    """
    Herschel-Bulkley model combines the effects of Bingham plastic and power-law behavior in a fluid
    """

    cuba_key = CUBA.HERSCHEL_BULKLEY_MODEL

    def __init__(self,
                 initial_viscosity=Default,
                 relaxation_time=Default,
                 linear_constant=Default,
                 power_law_index=Default,
                 *args,
                 **kwargs):
        super(HerschelBulkleyModel, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_initial_viscosity(initial_viscosity)
        self._init_models()
        self._init_relaxation_time(relaxation_time)
        self._init_linear_constant(linear_constant)
        self._init_power_law_index(power_law_index)

    def supported_parameters(self):
        try:
            base_params = super(HerschelBulkleyModel,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.INITIAL_VISCOSITY,
            CUBA.RELAXATION_TIME,
            CUBA.LINEAR_CONSTANT,
            CUBA.POWER_LAW_INDEX, ) + base_params

    def _init_definition(self):
        self._definition = "Herschel-Bulkley model combines the effects of Bingham plastic and power-law behavior in a fluid"

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
        import itertools
        value = validation.cast_data_type(value, 'CUBA.INITIAL_VISCOSITY')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.INITIAL_VISCOSITY')

        return value

    def _init_models(self):
        self._models = ['CUBA.CONTINUUM']

    @property
    def models(self):
        return self._models

    def _init_relaxation_time(self, value):
        if value is Default:
            value = 1.0

        self.relaxation_time = value

    @property
    def relaxation_time(self):
        return self.data[CUBA.RELAXATION_TIME]

    @relaxation_time.setter
    def relaxation_time(self, value):
        value = self._validate_relaxation_time(value)
        self.data[CUBA.RELAXATION_TIME] = value

    def _validate_relaxation_time(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.RELAXATION_TIME')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.RELAXATION_TIME')

        return value

    def _init_linear_constant(self, value):
        if value is Default:
            value = 1e-05

        self.linear_constant = value

    @property
    def linear_constant(self):
        return self.data[CUBA.LINEAR_CONSTANT]

    @linear_constant.setter
    def linear_constant(self, value):
        value = self._validate_linear_constant(value)
        self.data[CUBA.LINEAR_CONSTANT] = value

    def _validate_linear_constant(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.LINEAR_CONSTANT')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.LINEAR_CONSTANT')

        return value

    def _init_power_law_index(self, value):
        if value is Default:
            value = 1.0

        self.power_law_index = value

    @property
    def power_law_index(self):
        return self.data[CUBA.POWER_LAW_INDEX]

    @power_law_index.setter
    def power_law_index(self, value):
        value = self._validate_power_law_index(value)
        self.data[CUBA.POWER_LAW_INDEX] = value

    def _validate_power_law_index(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.POWER_LAW_INDEX')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.POWER_LAW_INDEX')

        return value
