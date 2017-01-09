from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class HexagonalLattice(BravaisLattice):
    """
    A hexagonal lattice
    """
    cuba_key = CUBA.HEXAGONAL_LATTICE

    def __init__(self, *args, **kwargs):

        super(HexagonalLattice, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(HexagonalLattice, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A hexagonal lattice"  # noqa
