from simphony.core import Default  # noqa
from . import validation
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem


class Bond(CUDSItem):
    """
    A bond between two or more atoms or particles
    """
    cuba_key = CUBA.BOND

    def __init__(self, particle):
        super(Bond, self).__init__()
        self._init_particle(particle)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Bond, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.PARTICLE, ) + base_params))

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
        validation.check_valid_shape(value, [None], 'PARTICLE')
        validation.check_elements(value, [None], 'PARTICLE')

        return value

    def _default_particle(self):
        raise TypeError("No default for particle")

    def _default_definition(self):
        return "A bond between two or more atoms or particles"  # noqa
