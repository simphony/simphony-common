from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class MultiphaseModel(PhysicsEquation):
    """
    Multiphase model
    """
    cuba_key = CUBA.MULTIPHASE_MODEL

    def __init__(self, *args, **kwargs):
        super(MultiphaseModel, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(MultiphaseModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "Multiphase model"  # noqa

    @property
    def definition(self):
        return self._definition
