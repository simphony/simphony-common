from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation


class MultiphaseModel(PhysicsEquation):
    """
    Multiphase model
    """
    cuba_key = CUBA.MULTIPHASE_MODEL

    def __init__(self, description=Default, name=Default):
        super(MultiphaseModel, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(MultiphaseModel, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_definition(self):
        return "Multiphase model"  # noqa
