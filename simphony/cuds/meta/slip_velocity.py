from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .constant_velocity_condition import ConstantVelocityCondition


class SlipVelocity(ConstantVelocityCondition):
    """
    Wall free slip velocity boundary condition
    """
    cuba_key = CUBA.SLIP_VELOCITY

    def __init__(self, velocity, material, description=Default, name=Default):
        super(SlipVelocity, self).__init__(
            velocity=velocity,
            material=material,
            description=description,
            name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(SlipVelocity, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_definition(self):
        return "Wall free slip velocity boundary condition"  # noqa
