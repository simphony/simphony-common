from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation


class RheologyModel(PhysicsEquation):
    """
    Rheology model of a CFD fluid
    """
    cuba_key = CUBA.RHEOLOGY_MODEL

    def __init__(self, description=Default, name=Default):

        super(RheologyModel, self).__init__(description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(RheologyModel, cls).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Rheology model of a CFD fluid"  # noqa
