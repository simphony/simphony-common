from .turbulence_model import TurbulenceModel
from simphony.core.cuba import CUBA


class LaminarFlowModel(TurbulenceModel):
    """
    ['Laminar model']
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

    def _init_models(self):
        self._models = ['CUBA.CONTINUUM']  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Laminar model"  # noqa

    @property
    def definition(self):
        return self._definition
