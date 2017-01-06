from .computational_method import ComputationalMethod
from simphony.core.cuba import CUBA


class Sph(ComputationalMethod):
    """
    ['Smooth particle hydrodynamics']
    """

    cuba_key = CUBA.SPH

    def __init__(self, *args, **kwargs):
        super(Sph, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_physics_equations()

    def supported_parameters(self):
        try:
            base_params = super(Sph, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "Smooth particle hydrodynamics"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_physics_equations(self):
        self._physics_equations = ['CUBA.CFD']  # noqa

    @property
    def physics_equations(self):
        return self._physics_equations
