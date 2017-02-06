from simphony.core import Default  # noqa
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class ComputationalModel(CUDSComponent):
    """
    Model category according to the RoMM
    """
    cuba_key = CUBA.COMPUTATIONAL_MODEL

    def __init__(self, description=Default, name=Default):
        super(ComputationalModel, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(ComputationalModel, cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([]) | base_params

    def _default_definition(self):
        return "Model category according to the RoMM"  # noqa
