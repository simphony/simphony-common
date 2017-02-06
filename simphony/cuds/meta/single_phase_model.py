from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .multiphase_model import MultiphaseModel


class SinglePhaseModel(MultiphaseModel):
    """
    A single phase fluid model
    """
    cuba_key = CUBA.SINGLE_PHASE_MODEL

    def __init__(self, description=Default, name=Default):
        super(SinglePhaseModel, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(SinglePhaseModel, cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([]) | base_params

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "A single phase fluid model"  # noqa
