from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation


class FreeSurfaceModel(PhysicsEquation):
    """
    Free surface model
    """
    cuba_key = CUBA.FREE_SURFACE_MODEL

    def __init__(self, description=Default, name=Default):

        super(FreeSurfaceModel, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(FreeSurfaceModel, cls).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Free surface model"  # noqa

    def _default_variables(self):
        return ['CUBA.SURFACE_TENSION']  # noqa
