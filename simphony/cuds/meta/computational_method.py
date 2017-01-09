from .solver_parameter import SolverParameter
from simphony.core.cuba import CUBA


class ComputationalMethod(SolverParameter):
    """
    A computational method according to the RoMM
    """
    cuba_key = CUBA.COMPUTATIONAL_METHOD

    def __init__(self, *args, **kwargs):

        super(ComputationalMethod, self).__init__(*args, **kwargs)
        self._init_physics_equations()

    def supported_parameters(self):
        try:
            base_params = super(ComputationalMethod,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A computational method according to the RoMM"  # noqa

    def _init_physics_equations(self):
        self._physics_equations = self._default_physics_equations()  # noqa

    @property
    def physics_equations(self):
        return self._physics_equations

    def _default_physics_equations(self):
        return []  # noqa
