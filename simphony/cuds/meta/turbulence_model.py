from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation


class TurbulenceModel(PhysicsEquation):
    """
    Turbulence model
    """
    cuba_key = CUBA.TURBULENCE_MODEL

    def __init__(self, description=Default, name=Default):
        super(TurbulenceModel, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(TurbulenceModel, cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([]) | base_params

    def _default_definition(self):
        return "Turbulence model"  # noqa
