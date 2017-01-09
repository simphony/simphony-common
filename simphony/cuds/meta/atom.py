from .particle import Particle
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class Atom(Particle):
    """
    An atom
    """
    cuba_key = CUBA.ATOM

    def __init__(self, mass=Default, *args, **kwargs):
        super(Atom, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_mass(mass)

    def supported_parameters(self):
        try:
            base_params = super(Atom, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.MASS, ) + base_params

    def _init_definition(self):
        self._definition = "An atom"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_mass(self, value):
        if value is Default:
            value = 1.0

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
