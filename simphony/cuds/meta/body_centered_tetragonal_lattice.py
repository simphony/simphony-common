from simphony.core import Default  # noqa
from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class BodyCenteredTetragonalLattice(BravaisLattice):
    """
    A body centered tetragonal lattice
    """
    cuba_key = CUBA.BODY_CENTERED_TETRAGONAL_LATTICE

    def __init__(self,
                 origin,
                 primitive_cell,
                 lattice_parameter=Default,
                 size=Default,
                 description=Default,
                 name=Default):
        super(BodyCenteredTetragonalLattice, self).__init__(
            lattice_parameter=lattice_parameter,
            origin=origin,
            primitive_cell=primitive_cell,
            size=size,
            description=description,
            name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(BodyCenteredTetragonalLattice,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_definition(self):
        return "A body centered tetragonal lattice"  # noqa
