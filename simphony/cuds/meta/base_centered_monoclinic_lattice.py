from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class BaseCenteredMonoclinicLattice(BravaisLattice):
    """
    A base centered monoclinic lattice
    """
    cuba_key = CUBA.BASE_CENTERED_MONOCLINIC_LATTICE

    def __init__(self, *args, **kwargs):

        super(BaseCenteredMonoclinicLattice, self).__init__(*args, **kwargs)
        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(BaseCenteredMonoclinicLattice,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A base centered monoclinic lattice"  # noqa
