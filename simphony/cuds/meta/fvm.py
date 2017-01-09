from .computational_method import ComputationalMethod
from simphony.core.cuba import CUBA


class Fvm(ComputationalMethod):
    """
    Finite volume method
    """
    cuba_key = CUBA.FVM

    def __init__(self, *args, **kwargs):

        super(Fvm, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(Fvm, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Finite volume method"  # noqa

    def _default_physics_equations(self):
        return ['CUBA.CFD']  # noqa
