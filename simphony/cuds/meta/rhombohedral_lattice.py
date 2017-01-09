from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class RhombohedralLattice(BravaisLattice):
    """
    A rhombohedral lattice
    """
    cuba_key = CUBA.RHOMBOHEDRAL_LATTICE

    def __init__(self, *args, **kwargs):

        super(RhombohedralLattice, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(RhombohedralLattice,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A rhombohedral lattice"  # noqa
