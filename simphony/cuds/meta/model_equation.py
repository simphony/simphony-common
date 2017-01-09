from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class ModelEquation(CUDSComponent):
    """
    The model equations are represented by all physics equations
    and material relations according to the RoMM
    """
    cuba_key = CUBA.MODEL_EQUATION

    def __init__(self, description=Default, name=Default):

        super(ModelEquation, self).__init__(description=description, name=name)
        self._init_models()
        self._init_variables()

    def supported_parameters(self):
        try:
            base_params = super(ModelEquation, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = self._default_models()  # noqa

    @property
    def models(self):
        return self._models

    def _default_models(self):
        return []  # noqa

    def _default_definition(self):
        return "The model equations are represented by all physics equations and material relations according to the RoMM"  # noqa

    def _init_variables(self):
        self._variables = self._default_variables()  # noqa

    @property
    def variables(self):
        return self._variables

    def _default_variables(self):
        return []  # noqa
