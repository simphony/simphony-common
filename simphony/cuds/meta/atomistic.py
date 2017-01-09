from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .computational_model import ComputationalModel


class Atomistic(ComputationalModel):
    """
    Atomistic model category according to the RoMM
    """
    cuba_key = CUBA.ATOMISTIC

    def __init__(self, description=Default, name=Default):

        super(Atomistic, self).__init__(description=description, name=name)

    def supported_parameters(self):
        try:
            base_params = super(Atomistic, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Atomistic model category according to the RoMM"  # noqa
