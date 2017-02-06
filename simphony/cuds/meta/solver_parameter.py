from simphony.core import Default  # noqa
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class SolverParameter(CUDSComponent):
    """
    Solver parameter and metadata
    """
    cuba_key = CUBA.SOLVER_PARAMETER

    def __init__(self, description=Default, name=Default):
        super(SolverParameter, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(SolverParameter, cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([]) | base_params

    def _default_definition(self):
        return "Solver parameter and metadata"  # noqa
