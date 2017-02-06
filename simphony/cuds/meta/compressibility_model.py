from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation


class CompressibilityModel(PhysicsEquation):
    """
    Compressibility model
    """
    cuba_key = CUBA.COMPRESSIBILITY_MODEL

    def __init__(self, description=Default, name=Default):
        super(CompressibilityModel, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(CompressibilityModel,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_definition(self):
        return "Compressibility model"  # noqa
