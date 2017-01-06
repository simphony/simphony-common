from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class OrthorhombicLattice(BravaisLattice):
    """
    An orthorhombic lattice
    """
    cuba_key = CUBA.ORTHORHOMBIC_LATTICE

    def __init__(self, *args, **kwargs):
        super(OrthorhombicLattice, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(OrthorhombicLattice,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "An orthorhombic lattice"  # noqa

    @property
    def definition(self):
        return self._definition
