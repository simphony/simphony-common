from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation


class KsDft(PhysicsEquation):
    """
    Kohn-Sham DFT equations
    """
    cuba_key = CUBA.KS_DFT

    def __init__(self, description=Default, name=Default):
        super(KsDft, self).__init__(description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(KsDft, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_models(self):
        return ['CUBA.ELECTRONIC']  # noqa

    def _default_definition(self):
        return "Kohn-Sham DFT equations"  # noqa

    def _default_variables(self):
        return [
            'CUBA.POSITION', 'CUBA.CHEMICAL_SPECIE', 'CUBA.ELECTRON_MASS',
            'CUBA.CHARGE_DENSITY', 'CUBA.ENERGY'
        ]  # noqa
