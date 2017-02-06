from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .point import Point


class Particle(Point):
    """
    A particle in a 3D space system
    """
    cuba_key = CUBA.PARTICLE

    def __init__(self, position=Default):
        super(Particle, self).__init__(position=position)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Particle, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_definition(self):
        return "A particle in a 3D space system"  # noqa
