from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class BodyCenteredTetragonalLattice(BravaisLattice):
    """
    ['A body centered tetragonal lattice']
    """

    cuba_key = CUBA.BODY_CENTERED_TETRAGONAL_LATTICE

    def __init__(self, *args, **kwargs):
        super(BodyCenteredTetragonalLattice, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(BodyCenteredTetragonalLattice,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "A body centered tetragonal lattice"  # noqa

    @property
    def definition(self):
        return self._definition
