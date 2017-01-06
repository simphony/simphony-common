from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class FaceCenteredCubicLattice(BravaisLattice):
    """
    A face centred cubic lattice
    """
    cuba_key = CUBA.FACE_CENTERED_CUBIC_LATTICE

    def __init__(self, *args, **kwargs):
        super(FaceCenteredCubicLattice, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(FaceCenteredCubicLattice,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "A face centred cubic lattice"  # noqa

    @property
    def definition(self):
        return self._definition
