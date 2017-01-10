from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .tetragonal_lattice import TetragonalLattice


class CubicLattice(TetragonalLattice):
    """
    A cubic lattice
    """
    cuba_key = CUBA.CUBIC_LATTICE

    def __init__(self,
                 primitive_cell,
                 origin,
                 lattice_parameter=Default,
                 size=Default,
                 description=Default,
                 name=Default):

        super(CubicLattice, self).__init__(
            lattice_parameter=lattice_parameter,
            primitive_cell=primitive_cell,
            size=size,
            origin=origin,
            description=description,
            name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(CubicLattice, cls).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A cubic lattice"  # noqa
