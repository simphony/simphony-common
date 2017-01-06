from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class TurbulenceModel(PhysicsEquation):
    """
    Turbulence model
    """
    cuba_key = CUBA.TURBULENCE_MODEL

    def __init__(self, *args, **kwargs):
        super(TurbulenceModel, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(TurbulenceModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "Turbulence model"  # noqa

    @property
    def definition(self):
        return self._definition
