from simphony.core.cuba import CUBA
from .tetragonal_lattice import TetragonalLattice


class CubicLattice(TetragonalLattice):
    """
    ['A cubic lattice']
    """

    cuba_key = CUBA.CUBIC_LATTICE

    def __init__(self, *args, **kwargs):
        super(CubicLattice, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(CubicLattice, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "A cubic lattice"  # noqa

    @property
    def definition(self):
        return self._definition
