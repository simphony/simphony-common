from simphony.core import Default  # noqa
from .computational_method import ComputationalMethod
from simphony.core.cuba import CUBA


class Fem(ComputationalMethod):
    """
    Finite element method
    """
    cuba_key = CUBA.FEM

    def __init__(self, description=Default, name=Default):
        super(Fem, self).__init__(description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Fem, cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([]) | base_params

    def _default_definition(self):
        return "Finite element method"  # noqa

    def _default_physics_equations(self):
        return ['CUBA.CFD']  # noqa
