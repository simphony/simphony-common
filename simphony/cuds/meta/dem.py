from .computational_method import ComputationalMethod
from simphony.core.cuba import CUBA


class Dem(ComputationalMethod):
    """
    ['Discrete element method']
    """

    cuba_key = CUBA.DEM

    def __init__(self, *args, **kwargs):
        super(Dem, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_physics_equations()

    def supported_parameters(self):
        try:
            base_params = super(Dem, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "Discrete element method"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_physics_equations(self):
        self._physics_equations = ['CUBA.GRANULAR_DYNAMICS']  # noqa

    @property
    def physics_equations(self):
        return self._physics_equations
