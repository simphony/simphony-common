from .turbulence_model import TurbulenceModel
from simphony.core.cuba import CUBA


class LaminarFlowModel(TurbulenceModel):
    """
    Laminar model
    """
    cuba_key = CUBA.LAMINAR_FLOW_MODEL

    def __init__(self, description=Default, name=Default):

        super(LaminarFlowModel, self).__init__(
            description=description, name=name)

    def supported_parameters(self):
        try:
            base_params = super(LaminarFlowModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Laminar model"  # noqa
