from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class TetragonalLattice(BravaisLattice):
    """
    A tetragonal lattice
    """
    cuba_key = CUBA.TETRAGONAL_LATTICE

    def __init__(self, *args, **kwargs):

        super(TetragonalLattice, self).__init__(*args, **kwargs)
        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(TetragonalLattice, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A tetragonal lattice"  # noqa
