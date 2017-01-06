from simphony.core.cuba import CUBA
from .thermal_model import ThermalModel


class IsothermalModel(ThermalModel):
    """
    Isothermal heat transport model, no transport of heat is assumed
    """

    cuba_key = CUBA.ISOTHERMAL_MODEL

    def __init__(self, *args, **kwargs):
        super(IsothermalModel, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_variables()

    def supported_parameters(self):
        try:
            base_params = super(IsothermalModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = ['CUBA.CONTINUUM']

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Isothermal heat transport model, no transport of heat is assumed"

    @property
    def definition(self):
        return self._definition

    def _init_variables(self):
        self._variables = []

    @property
    def variables(self):
        return self._variables
