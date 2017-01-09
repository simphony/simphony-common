from .multiphase_model import MultiphaseModel
from simphony.core.cuba import CUBA


class SinglePhaseModel(MultiphaseModel):
    """
    A single phase fluid model
    """
    cuba_key = CUBA.SINGLE_PHASE_MODEL

    def __init__(self, *args, **kwargs):

        super(SinglePhaseModel, self).__init__(*args, **kwargs)
        self._init_models()
        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(SinglePhaseModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa    

    def _default_definition(self):
        return "A single phase fluid model"  # noqa
