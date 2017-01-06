from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class ThermalModel(PhysicsEquation):
    """
    Non-isothermal heat transport model
    """
    cuba_key = CUBA.THERMAL_MODEL

    def __init__(self, *args, **kwargs):
        super(ThermalModel, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_variables()

    def supported_parameters(self):
        try:
            base_params = super(ThermalModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = ['CUBA.CONTINUUM']  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Non-isothermal heat transport model"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_variables(self):
        self._variables = ['CUBA.TEMPERATURE',
                           'CUBA.HEAT_CONDUCTIVITY']  # noqa

    @property
    def variables(self):
        return self._variables
