from .cuds_item import CUDSItem
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class Bond(CUDSItem):
    """
    A bond between two or more atoms or particles
    """
    cuba_key = CUBA.BOND

    def __init__(self, particle, *args, **kwargs):
        super(Bond, self).__init__(*args, **kwargs)

        self._init_particle(particle)
        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(Bond, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.PARTICLE, ) + base_params

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

        value = validation.cast_data_type(value, 'PARTICLE')
        validation.check_shape(value, [None])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if hasattr(container, "flatten"):
            flat_array = value.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'PARTICLE')

        return value

    def _init_definition(self):
        self._definition = "A bond between two or more atoms or particles"  # noqa

    @property
    def definition(self):
        return self._definition
