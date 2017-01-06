from .compressibility_model import CompressibilityModel
from simphony.core.cuba import CUBA


class IncompressibleFluidModel(CompressibilityModel):
    """
    ['Incompressible fluid model']
    """

    cuba_key = CUBA.INCOMPRESSIBLE_FLUID_MODEL

    def __init__(self, *args, **kwargs):
        super(IncompressibleFluidModel, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_variables()

    def supported_parameters(self):
        try:
            base_params = super(IncompressibleFluidModel,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = ['CUBA.CONTINUUM']  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Incompressible fluid model"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_variables(self):
        self._variables = [
            'CUBA.VELOCITY', 'CUBA.POSITION', 'CUBA.DENSITY', 'CUBA.VISCOSITY'
        ]  # noqa

    @property
    def variables(self):
        return self._variables
