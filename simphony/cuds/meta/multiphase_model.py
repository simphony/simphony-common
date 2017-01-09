from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class MultiphaseModel(PhysicsEquation):
    """
    Multiphase model
    """
    cuba_key = CUBA.MULTIPHASE_MODEL

    def __init__(self, description=Default, name=Default):

        super(MultiphaseModel, self).__init__(
            description=description, name=name)

    def supported_parameters(self):
        try:
            base_params = super(MultiphaseModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Multiphase model"  # noqa
