from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .tetragonal_lattice import TetragonalLattice


class CubicLattice(TetragonalLattice):
    """
    A cubic lattice
    """
    cuba_key = CUBA.CUBIC_LATTICE

    def __init__(self,
                 origin,
                 primitive_cell,
                 lattice_parameter=Default,
                 size=Default,
                 description=Default,
                 name=Default):
        super(CubicLattice, self).__init__(
            lattice_parameter=lattice_parameter,
            origin=origin,
            primitive_cell=primitive_cell,
            size=size,
            description=description,
            name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(CubicLattice, cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([]) | base_params

    def _default_definition(self):
        return "A cubic lattice"  # noqa
