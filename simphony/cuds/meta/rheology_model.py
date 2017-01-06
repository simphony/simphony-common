from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class RheologyModel(PhysicsEquation):
    """
    ['Rheology model of a CFD fluid']
    """

    cuba_key = CUBA.RHEOLOGY_MODEL

    def __init__(self, *args, **kwargs):
        super(RheologyModel, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(RheologyModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = ['CUBA.CONTINUUM']  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Rheology model of a CFD fluid"  # noqa

    @property
    def definition(self):
        return self._definition
