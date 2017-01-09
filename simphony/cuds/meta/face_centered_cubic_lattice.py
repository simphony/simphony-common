from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class FaceCenteredCubicLattice(BravaisLattice):
    """
    A face centred cubic lattice
    """
    cuba_key = CUBA.FACE_CENTERED_CUBIC_LATTICE

    def __init__(self, *args, **kwargs):

        super(FaceCenteredCubicLattice, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(FaceCenteredCubicLattice,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A face centred cubic lattice"  # noqa
