from .computational_method import ComputationalMethod
from simphony.core.cuba import CUBA


class Verlet(ComputationalMethod):
    """
    Newtonian dynamics integration using verlet algorithm
    """
    cuba_key = CUBA.VERLET

    def __init__(self, *args, **kwargs):

        super(Verlet, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(Verlet, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Newtonian dynamics integration using verlet algorithm"  # noqa

    def _default_physics_equations(self):
        return ['CUBA.MOLECULAR_DYNAMICS']  # noqa
