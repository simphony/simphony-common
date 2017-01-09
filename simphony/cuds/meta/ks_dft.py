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

    def _default_models(self):
        return ['CUBA.ELECTRONIC']  # noqa    

    def _default_definition(self):
        return "Kohn-Sham DFT equations"  # noqa    

    def _default_variables(self):
        return [
            'CUBA.POSITION', 'CUBA.CHEMICAL_SPECIE', 'CUBA.ELECTRON_MASS',
            'CUBA.CHARGE_DENSITY', 'CUBA.ENERGY'
        ]  # noqa
