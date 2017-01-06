from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class ElectrostaticModel(PhysicsEquation):
    """
    ['Electrostatic model']
    """

    cuba_key = CUBA.ELECTROSTATIC_MODEL

    def __init__(self, *args, **kwargs):
        super(ElectrostaticModel, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(ElectrostaticModel,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = []  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Electrostatic model"  # noqa

    @property
    def definition(self):
        return self._definition
