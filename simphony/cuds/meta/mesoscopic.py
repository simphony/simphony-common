from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .computational_model import ComputationalModel


class Mesoscopic(ComputationalModel):
    """
    Mesoscopic model category according to the RoMM
    """
    cuba_key = CUBA.MESOSCOPIC

    def __init__(self, description=Default, name=Default):
        super(Mesoscopic, self).__init__(description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Mesoscopic, cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([]) | base_params

    def _default_definition(self):
        return "Mesoscopic model category according to the RoMM"  # noqa
