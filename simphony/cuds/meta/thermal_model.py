from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation


class ThermalModel(PhysicsEquation):
    """
    Non-isothermal heat transport model
    """
    cuba_key = CUBA.THERMAL_MODEL

    def __init__(self, description=Default, name=Default):
        super(ThermalModel, self).__init__(description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(ThermalModel, cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([]) | base_params

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Non-isothermal heat transport model"  # noqa

    def _default_variables(self):
        return ['CUBA.TEMPERATURE', 'CUBA.HEAT_CONDUCTIVITY']  # noqa
