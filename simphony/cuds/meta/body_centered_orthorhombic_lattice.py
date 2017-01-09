from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class BodyCenteredOrthorhombicLattice(BravaisLattice):
    """
    A body centered orthorhombic lattice
    """
    cuba_key = CUBA.BODY_CENTERED_ORTHORHOMBIC_LATTICE

    def __init__(self, *args, **kwargs):

        super(BodyCenteredOrthorhombicLattice, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(BodyCenteredOrthorhombicLattice,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A body centered orthorhombic lattice"  # noqa
