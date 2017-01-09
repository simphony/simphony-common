from simphony.core import Default  # noqa
from .data_set import DataSet
from simphony.core.cuba import CUBA


class Lattice(DataSet):
    """
    A lattice
    """
    cuba_key = CUBA.LATTICE

    def __init__(self, description=Default, name=Default):

        super(Lattice, self).__init__(description=description, name=name)

    def supported_parameters(self):
        try:
            base_params = super(Lattice, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A lattice"  # noqa
