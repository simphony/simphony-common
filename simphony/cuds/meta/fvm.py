from .computational_method import ComputationalMethod
from simphony.core.cuba import CUBA


class Fvm(ComputationalMethod):
    """
    ['Finite volume method']
    """

    cuba_key = CUBA.FVM

    def __init__(self, *args, **kwargs):
        super(Fvm, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_physics_equations()

    def supported_parameters(self):
        try:
            base_params = super(Fvm, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "Finite volume method"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_physics_equations(self):
        self._physics_equations = ['CUBA.CFD']  # noqa

    @property
    def physics_equations(self):
        return self._physics_equations
