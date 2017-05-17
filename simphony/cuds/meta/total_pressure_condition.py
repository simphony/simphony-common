from simphony.core import Default  # noqa
from .mixed_condition import MixedCondition
from simphony.core.cuba import CUBA
from simphony.cuds import meta_validation


class TotalPressureCondition(MixedCondition):
    """
    Total pressure boundary condition
    """
    cuba_key = CUBA.TOTAL_PRESSURE_CONDITION

    def __init__(self,
                 dynamic_pressure,
                 material,
                 description=Default,
                 name=Default):
        super(TotalPressureCondition, self).__init__(
            material=material, description=description, name=name)
        self._init_models()
        self._init_variables()
        self._init_dynamic_pressure(dynamic_pressure)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(TotalPressureCondition,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.DYNAMIC_PRESSURE, ) + base_params))

    def _init_models(self):
        self._models = self._default_models()  # noqa

    @property
    def models(self):
        return self._models

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Total pressure boundary condition"  # noqa

    def _init_variables(self):
        self._variables = self._default_variables()  # noqa

    @property
    def variables(self):
        return self._variables

    def _default_variables(self):
        return ['CUBA.DYNAMIC_PRESSURE']  # noqa

    def _init_dynamic_pressure(self, value):
        if value is Default:
            value = self._default_dynamic_pressure()

        self.dynamic_pressure = value

    @property
    def dynamic_pressure(self):
        return self.data[CUBA.DYNAMIC_PRESSURE]

    @dynamic_pressure.setter
    def dynamic_pressure(self, value):
        value = self._validate_dynamic_pressure(value)
        self.data[CUBA.DYNAMIC_PRESSURE] = value

    def _validate_dynamic_pressure(self, value):
        value = meta_validation.cast_data_type(value, 'DYNAMIC_PRESSURE')
        meta_validation.check_valid_shape(value, [1], 'DYNAMIC_PRESSURE')
        meta_validation.validate_cuba_keyword(value, 'DYNAMIC_PRESSURE')
        return value

    def _default_dynamic_pressure(self):
        raise TypeError("No default for dynamic_pressure")
