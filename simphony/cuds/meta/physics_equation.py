from .model_equation import ModelEquation
from simphony.core.cuba import CUBA


class PhysicsEquation(ModelEquation):
    """
    Physics equation
    """
    cuba_key = CUBA.PHYSICS_EQUATION

    def __init__(self, *args, **kwargs):
        super(PhysicsEquation, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(PhysicsEquation, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "Physics equation"  # noqa

    @property
    def definition(self):
        return self._definition
