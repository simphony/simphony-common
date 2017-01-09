from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class CompressibilityModel(PhysicsEquation):
    """
    Compressibility model
    """
    cuba_key = CUBA.COMPRESSIBILITY_MODEL

    def __init__(self, *args, **kwargs):

        super(CompressibilityModel, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(CompressibilityModel,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Compressibility model"  # noqa
