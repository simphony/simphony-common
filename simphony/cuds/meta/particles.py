from simphony.core import Default  # noqa
from .data_set import DataSet
from simphony.core.cuba import CUBA
from simphony.cuds import meta_validation


class Particles(DataSet):
    """
    A collection of particles
    """
    cuba_key = CUBA.PARTICLES

    def __init__(self, bond, particle, description=Default, name=Default):
        super(Particles, self).__init__(description=description, name=name)
        self._init_particle(particle)
        self._init_bond(bond)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Particles, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((
            CUBA.PARTICLE,
            CUBA.BOND, ) + base_params))

    def _init_particle(self, value):
        if value is Default:
            value = self._default_particle()

        self.particle = value

    @property
    def particle(self):
        return self.data[CUBA.PARTICLE]

    @particle.setter
    def particle(self, value):
        value = self._validate_particle(value)
        self.data[CUBA.PARTICLE] = value

    def _validate_particle(self, value):
        value = meta_validation.cast_data_type(value, 'PARTICLE')
        meta_validation.check_valid_shape(value, [None], 'PARTICLE')
        meta_validation.check_elements(value, [None], 'PARTICLE')

        return value

    def _default_particle(self):
        raise TypeError("No default for particle")

    def _default_definition(self):
        return "A collection of particles"  # noqa

    def _init_bond(self, value):
        if value is Default:
            value = self._default_bond()

        self.bond = value

    @property
    def bond(self):
        return self.data[CUBA.BOND]

    @bond.setter
    def bond(self, value):
        value = self._validate_bond(value)
        self.data[CUBA.BOND] = value

    def _validate_bond(self, value):
        value = meta_validation.cast_data_type(value, 'BOND')
        meta_validation.check_valid_shape(value, [None], 'BOND')
        meta_validation.check_elements(value, [None], 'BOND')

        return value

    def _default_bond(self):
        raise TypeError("No default for bond")
