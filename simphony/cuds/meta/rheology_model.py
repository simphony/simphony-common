from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class RheologyModel(PhysicsEquation):
    """
    Rheology model of a CFD fluid
    """
    cuba_key = CUBA.RHEOLOGY_MODEL

    def __init__(self, description=Default, name=Default):

        super(RheologyModel, self).__init__(description=description, name=name)

    def supported_parameters(self):
        try:
            base_params = super(RheologyModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Rheology model of a CFD fluid"  # noqa
