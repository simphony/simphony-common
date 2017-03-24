from simphony.core import Default  # noqa
from simphony.cuds import meta_validation
from simphony.core.cuba import CUBA
from .dirichlet import Dirichlet


class ConstantPressureCondition(Dirichlet):
    """
    Constant pressure condition
    """
    cuba_key = CUBA.CONSTANT_PRESSURE_CONDITION

    def __init__(self, pressure, material, description=Default, name=Default):
        super(ConstantPressureCondition, self).__init__(
            material=material, description=description, name=name)
        self._init_models()
        self._init_pressure(pressure)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(ConstantPressureCondition,
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
        return "Constant pressure condition"  # noqa

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
