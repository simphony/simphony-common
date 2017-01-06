from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class MolecularStatics(PhysicsEquation):
    """
    Classical atomistic static molecular model
    """

    cuba_key = CUBA.MOLECULAR_STATICS

    def __init__(self, *args, **kwargs):
        super(MolecularStatics, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_variables()

    def supported_parameters(self):
        try:
            base_params = super(MolecularStatics, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = ['CUBA.ATOMISTIC']

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Classical atomistic static molecular model"

    @property
    def definition(self):
        return self._definition

    def _init_variables(self):
        self._variables = ['CUBA.POSITION', 'CUBA.FORCE']

    @property
    def variables(self):
        return self._variables
