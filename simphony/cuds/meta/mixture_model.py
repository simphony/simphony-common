from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation


class MixtureModel(PhysicsEquation):
    """
    Mixture (drift flux) model
    """
    cuba_key = CUBA.MIXTURE_MODEL

    def __init__(self, description=Default, name=Default):

        super(MixtureModel, self).__init__(description=description, name=name)

    def supported_parameters(self):
        try:
            base_params = super(MixtureModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Mixture (drift flux) model"  # noqa
