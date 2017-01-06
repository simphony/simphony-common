from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class MonoclinicLattice(BravaisLattice):
    """
    ['A monoclinic lattice']
    """

    cuba_key = CUBA.MONOCLINIC_LATTICE

    def __init__(self, *args, **kwargs):
        super(MonoclinicLattice, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(MonoclinicLattice, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "A monoclinic lattice"  # noqa

    @property
    def definition(self):
        return self._definition
