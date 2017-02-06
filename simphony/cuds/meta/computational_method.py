from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .solver_parameter import SolverParameter


class ComputationalMethod(SolverParameter):
    """
    A computational method according to the RoMM
    """
    cuba_key = CUBA.COMPUTATIONAL_METHOD

    def __init__(self, description=Default, name=Default):
        super(ComputationalMethod, self).__init__(
            description=description, name=name)
        self._init_physics_equations()

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(ComputationalMethod,
                                cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([]) | base_params

    def _default_definition(self):
        return "A computational method according to the RoMM"  # noqa

    def _init_physics_equations(self):
        self._physics_equations = self._default_physics_equations()  # noqa

    @property
    def physics_equations(self):
        return self._physics_equations

    def _default_physics_equations(self):
        return []  # noqa
