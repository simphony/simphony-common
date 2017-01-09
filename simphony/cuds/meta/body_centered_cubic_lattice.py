from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class BodyCenteredCubicLattice(BravaisLattice):
    """
    A body centred cubic lattice
    """
    cuba_key = CUBA.BODY_CENTERED_CUBIC_LATTICE

    def __init__(self, *args, **kwargs):

        super(BodyCenteredCubicLattice, self).__init__(*args, **kwargs)
        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(BodyCenteredCubicLattice,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A body centred cubic lattice"  # noqa
