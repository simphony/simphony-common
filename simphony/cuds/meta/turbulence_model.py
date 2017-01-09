from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class TurbulenceModel(PhysicsEquation):
    """
    Turbulence model
    """
    cuba_key = CUBA.TURBULENCE_MODEL

    def __init__(self, description=Default, name=Default):

        super(TurbulenceModel, self).__init__(
            description=description, name=name)

    def supported_parameters(self):
        try:
            base_params = super(TurbulenceModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Turbulence model"  # noqa
