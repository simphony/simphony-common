from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class KsDft(PhysicsEquation):
    """
    Kohn-Sham DFT equations
    """
    cuba_key = CUBA.KS_DFT

    def __init__(self, *args, **kwargs):
        super(KsDft, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_variables()

    def supported_parameters(self):
        try:
            base_params = super(KsDft, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = ['CUBA.ELECTRONIC']  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Kohn-Sham DFT equations"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_variables(self):
        self._variables = [
            'CUBA.POSITION', 'CUBA.CHEMICAL_SPECIE', 'CUBA.ELECTRON_MASS',
            'CUBA.CHARGE_DENSITY', 'CUBA.ENERGY'
        ]  # noqa

    @property
    def variables(self):
        return self._variables
