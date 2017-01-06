from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class ModelEquation(CUDSComponent):
    """
    The model equations are represented by all physics equations and material relations according to the RoMM
    """

    cuba_key = CUBA.MODEL_EQUATION

    def __init__(self, *args, **kwargs):
        super(ModelEquation, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_variables()

    def supported_parameters(self):
        try:
            base_params = super(ModelEquation, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = []

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "The model equations are represented by all physics equations and material relations according to the RoMM"

    @property
    def definition(self):
        return self._definition

    def _init_variables(self):
        self._variables = []

    @property
    def variables(self):
        return self._variables
