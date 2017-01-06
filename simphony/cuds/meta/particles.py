from simphony.core import Default
from . import validation
from .data_set import DataSet
from simphony.core.cuba import CUBA


class Particles(DataSet):
    """
    A collection of particles
    """
    cuba_key = CUBA.PARTICLES

    def __init__(self, particle, bond, *args, **kwargs):
        super(Particles, self).__init__(*args, **kwargs)

        self._init_particle(particle)
        self._init_definition()
        self._init_bond(bond)

    def supported_parameters(self):
        try:
            base_params = super(Particles, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.PARTICLE,
            CUBA.BOND, ) + base_params

    def _init_particle(self, value):
        if value is Default:
            raise TypeError("Value for particle must be specified")

        self.particle = value

    @property
    def particle(self):
        return self.data[CUBA.PARTICLE]

    @particle.setter
    def particle(self, value):
        value = self._validate_particle(value)
        self.data[CUBA.PARTICLE] = value

    def _validate_particle(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.PARTICLE')
        validation.check_shape(value, [None])
        for tuple_ in itertools.product(*[range(x) for x in [None]]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.PARTICLE')

        return value

    def _init_definition(self):
        self._definition = "A collection of particles"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_bond(self, value):
        if value is Default:
            raise TypeError("Value for bond must be specified")

        self.bond = value

    @property
    def bond(self):
        return self.data[CUBA.BOND]

    @bond.setter
    def bond(self, value):
        value = self._validate_bond(value)
        self.data[CUBA.BOND] = value

    def _validate_bond(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.BOND')
        validation.check_shape(value, [None])
        for tuple_ in itertools.product(*[range(x) for x in [None]]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.BOND')

        return value
