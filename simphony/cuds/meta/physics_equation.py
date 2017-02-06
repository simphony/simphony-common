from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .model_equation import ModelEquation


class PhysicsEquation(ModelEquation):
    """
    Physics equation
    """
    cuba_key = CUBA.PHYSICS_EQUATION

    def __init__(self, description=Default, name=Default):
        super(PhysicsEquation, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(PhysicsEquation, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_definition(self):
        return "Physics equation"  # noqa
