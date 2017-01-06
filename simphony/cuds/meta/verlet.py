from .computational_method import ComputationalMethod
from simphony.core.cuba import CUBA


class Verlet(ComputationalMethod):
    """
    Newtonian dynamics integration using verlet algorithm
    """
    cuba_key = CUBA.VERLET

    def __init__(self, *args, **kwargs):
        super(Verlet, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_physics_equations()

    def supported_parameters(self):
        try:
            base_params = super(Verlet, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "Newtonian dynamics integration using verlet algorithm"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_physics_equations(self):
        self._physics_equations = ['CUBA.MOLECULAR_DYNAMICS']  # noqa

    @property
    def physics_equations(self):
        return self._physics_equations
