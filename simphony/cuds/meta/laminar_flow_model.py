from .turbulence_model import TurbulenceModel
from simphony.core.cuba import CUBA


class LaminarFlowModel(TurbulenceModel):
    """
    Laminar model
    """
    cuba_key = CUBA.LAMINAR_FLOW_MODEL

    def __init__(self, *args, **kwargs):

        super(LaminarFlowModel, self).__init__(*args, **kwargs)
        self._init_models()
        self._init_definition()

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
