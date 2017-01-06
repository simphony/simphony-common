from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class FreeSurfaceModel(PhysicsEquation):
    """
    Free surface model
    """
    cuba_key = CUBA.FREE_SURFACE_MODEL

    def __init__(self, *args, **kwargs):
        super(FreeSurfaceModel, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_variables()

    def supported_parameters(self):
        try:
            base_params = super(FreeSurfaceModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = ['CUBA.CONTINUUM']  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Free surface model"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_variables(self):
        self._variables = ['CUBA.SURFACE_TENSION']  # noqa

    @property
    def variables(self):
        return self._variables
