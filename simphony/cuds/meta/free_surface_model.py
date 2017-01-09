from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class FreeSurfaceModel(PhysicsEquation):
    """
    Free surface model
    """
    cuba_key = CUBA.FREE_SURFACE_MODEL

    def __init__(self, *args, **kwargs):

        super(FreeSurfaceModel, self).__init__(*args, **kwargs)
        self._init_models()
        self._init_definition()
        self._init_variables()

    def supported_parameters(self):
        try:
            base_params = super(FreeSurfaceModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa    

    def _default_definition(self):
        return "Free surface model"  # noqa    

    def _default_variables(self):
        return ['CUBA.SURFACE_TENSION']  # noqa
