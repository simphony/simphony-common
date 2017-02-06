from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .computational_model import ComputationalModel


class Electronic(ComputationalModel):
    """
    Electronic model category according to the RoMM
    """
    cuba_key = CUBA.ELECTRONIC

    def __init__(self, description=Default, name=Default):
        super(Electronic, self).__init__(description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Electronic, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return () + base_params

    def _default_definition(self):
        return "Electronic model category according to the RoMM"  # noqa
