from simphony.core import Default  # noqa
from . import validation
from .data_set import DataSet
from simphony.core.cuba import CUBA


class Particles(DataSet):
    """
    A collection of particles
    """
    cuba_key = CUBA.PARTICLES

    def __init__(self, particle, bond, description=Default, name=Default):

        super(Particles, self).__init__(description=description, name=name)
        self._init_particle(particle)
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
        value = validation.cast_data_type(value, 'PARTICLE')
        validation.check_shape_at_least(value, [None])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if hasattr(value, "flatten"):
            flat_array = value.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'PARTICLE')

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
        value = validation.cast_data_type(value, 'BOND')
        validation.check_shape_at_least(value, [None])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if hasattr(value, "flatten"):
            flat_array = value.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'BOND')

        return value

    def _default_bond(self):
        raise TypeError("No default for bond")
