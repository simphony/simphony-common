from .computational_model import ComputationalModel
from simphony.core.cuba import CUBA


class Continuum(ComputationalModel):
    """
    Continuum model category according to the RoMM
    """
    cuba_key = CUBA.CONTINUUM

    def __init__(self, description=Default, name=Default):

        super(Continuum, self).__init__(description=description, name=name)

    def supported_parameters(self):
        try:
            base_params = super(Continuum, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Continuum model category according to the RoMM"  # noqa
