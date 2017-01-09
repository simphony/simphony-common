from simphony.core import Default  # noqa
from . import validation
from simphony.core.cuba import CUBA
from .particle import Particle


class Atom(Particle):
    """
    An atom
    """
    cuba_key = CUBA.ATOM

    def __init__(self, mass, position=Default):

        super(Atom, self).__init__(position=position)
        self._init_mass(mass)

    def supported_parameters(self):
        try:
            base_params = super(Atom, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.MASS, ) + base_params

    def _default_definition(self):
        return "An atom"  # noqa

    def _init_mass(self, value):
        if value is Default:
            value = self._default_mass()

        self.mass = value

    @property
    def mass(self):
        return self.data[CUBA.MASS]

    @mass.setter
    def mass(self, value):
        value = self._validate_mass(value)
        self.data[CUBA.MASS] = value

    def _validate_mass(self, value):
        value = validation.cast_data_type(value, 'MASS')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'MASS')
        return value

    def _default_mass(self):
        return 1.0
