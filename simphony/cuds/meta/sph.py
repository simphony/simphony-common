from simphony.core import Default  # noqa
from .computational_method import ComputationalMethod
from simphony.core.cuba import CUBA


class Sph(ComputationalMethod):
    """
    Smooth particle hydrodynamics
    """
    cuba_key = CUBA.SPH

    def __init__(self, description=Default, name=Default):
        super(Sph, self).__init__(description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Sph, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_definition(self):
        return "Smooth particle hydrodynamics"  # noqa

    def _default_physics_equations(self):
        return ['CUBA.CFD']  # noqa
