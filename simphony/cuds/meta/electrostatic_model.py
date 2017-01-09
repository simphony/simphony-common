from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class ElectrostaticModel(PhysicsEquation):
    """
    Electrostatic model
    """
    cuba_key = CUBA.ELECTROSTATIC_MODEL

    def __init__(self, description=Default, name=Default):

        super(ElectrostaticModel, self).__init__(
            description=description, name=name)

    def supported_parameters(self):
        try:
            base_params = super(ElectrostaticModel,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return []  # noqa

    def _default_definition(self):
        return "Electrostatic model"  # noqa
