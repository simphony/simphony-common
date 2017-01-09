from .computational_method import ComputationalMethod
from simphony.core.cuba import CUBA


class Sph(ComputationalMethod):
    """
    Smooth particle hydrodynamics
    """
    cuba_key = CUBA.SPH

    def __init__(self, *args, **kwargs):

        super(Sph, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(Sph, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Smooth particle hydrodynamics"  # noqa

    def _default_physics_equations(self):
        return ['CUBA.CFD']  # noqa
