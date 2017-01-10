from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .turbulence_model import TurbulenceModel


class LaminarFlowModel(TurbulenceModel):
    """
    Laminar model
    """
    cuba_key = CUBA.LAMINAR_FLOW_MODEL

    def __init__(self, description=Default, name=Default):

        super(LaminarFlowModel, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(LaminarFlowModel, cls).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Laminar model"  # noqa
