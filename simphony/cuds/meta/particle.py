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

    def supported_parameters(self):
        try:
            base_params = super(Particle, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A particle in a 3D space system"  # noqa
