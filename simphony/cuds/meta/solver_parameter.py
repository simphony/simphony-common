from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class SolverParameter(CUDSComponent):
    """
    Solver parameter and metadata
    """
    cuba_key = CUBA.SOLVER_PARAMETER

    def __init__(self, *args, **kwargs):

        super(SolverParameter, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(SolverParameter, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Solver parameter and metadata"  # noqa
