from simphony.core.cuba import CUBA
from .thermal_model import ThermalModel


class IsothermalModel(ThermalModel):
    """
    Isothermal heat transport model, no transport of heat is
    assumed
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

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa    

    def _default_definition(self):
        return "Isothermal heat transport model, no transport of heat is assumed"  # noqa    

    def _default_variables(self):
        return []  # noqa
