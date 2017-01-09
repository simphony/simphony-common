from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class ThermalModel(PhysicsEquation):
    """
    Non-isothermal heat transport model
    """
    cuba_key = CUBA.THERMAL_MODEL

    def __init__(self, *args, **kwargs):

        super(ThermalModel, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(ThermalModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Non-isothermal heat transport model"  # noqa

    def _default_variables(self):
        return ['CUBA.TEMPERATURE', 'CUBA.HEAT_CONDUCTIVITY']  # noqa
