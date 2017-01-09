from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class TriclinicLattice(BravaisLattice):
    """
    A triclinic lattice
    """
    cuba_key = CUBA.TRICLINIC_LATTICE

    def __init__(self, *args, **kwargs):

        super(TriclinicLattice, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(TriclinicLattice, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A triclinic lattice"  # noqa
