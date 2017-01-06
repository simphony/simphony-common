from .data_set import DataSet
from simphony.core.cuba import CUBA


class Lattice(DataSet):
    """
    A lattice
    """

    cuba_key = CUBA.LATTICE

    def __init__(self, *args, **kwargs):
        super(Lattice, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(Lattice, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "A lattice"

    @property
    def definition(self):
        return self._definition
