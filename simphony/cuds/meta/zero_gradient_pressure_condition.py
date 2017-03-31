from simphony.core import Default  # noqa
from .neumann import Neumann
from simphony.core.cuba import CUBA
from simphony.cuds import meta_validation


class ZeroGradientPressureCondition(Neumann):
    """
    Zero gradient pressure condition
    """
    cuba_key = CUBA.ZERO_GRADIENT_PRESSURE_CONDITION

    def __init__(self, pressure, material, description=Default, name=Default):
        super(ZeroGradientPressureCondition, self).__init__(
            material=material, description=description, name=name)
        self._init_models()
        self._init_variables()
        self._init_pressure(pressure)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(ZeroGradientPressureCondition,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.PRESSURE, ) + base_params))

    def _init_models(self):
        self._models = self._default_models()  # noqa

    @property
    def models(self):
        return self._models

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Zero gradient pressure condition"  # noqa

    def _init_variables(self):
        self._variables = self._default_variables()  # noqa

    @property
    def variables(self):
        return self._variables

    def _default_variables(self):
        return ['CUBA.PRESSURE']  # noqa

    def _init_pressure(self, value):
        if value is Default:
            value = self._default_pressure()

        self.pressure = value

    @property
    def pressure(self):
        return self.data[CUBA.PRESSURE]

    @pressure.setter
    def pressure(self, value):
        value = self._validate_pressure(value)
        self.data[CUBA.PRESSURE] = value

    def _validate_pressure(self, value):
        value = meta_validation.cast_data_type(value, 'PRESSURE')
        meta_validation.check_valid_shape(value, [1], 'PRESSURE')
        meta_validation.validate_cuba_keyword(value, 'PRESSURE')
        return value

    def _default_pressure(self):
        raise TypeError("No default for pressure")
