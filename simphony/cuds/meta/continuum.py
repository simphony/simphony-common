from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .computational_model import ComputationalModel


class Continuum(ComputationalModel):
    """
    Continuum model category according to the RoMM
    """
    cuba_key = CUBA.CONTINUUM

    def __init__(self, description=Default, name=Default):
        super(Continuum, self).__init__(description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Continuum, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_definition(self):
        return "Continuum model category according to the RoMM"  # noqa
