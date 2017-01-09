from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class OrthorhombicLattice(BravaisLattice):
    """
    An orthorhombic lattice
    """
    cuba_key = CUBA.ORTHORHOMBIC_LATTICE

    def __init__(self, *args, **kwargs):

        super(OrthorhombicLattice, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(OrthorhombicLattice,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "An orthorhombic lattice"  # noqa
