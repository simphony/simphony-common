from simphony.core import Default  # noqa
from .computational_method import ComputationalMethod
from simphony.core.cuba import CUBA


class Fvm(ComputationalMethod):
    """
    Finite volume method
    """
    cuba_key = CUBA.FVM

    def __init__(self, description=Default, name=Default):

        super(Fvm, self).__init__(description=description, name=name)

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
