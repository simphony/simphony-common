from simphony.core import Default  # noqa
from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class BaseCenteredOrthorhombicLattice(BravaisLattice):
    """
    A base centered orthorhombic lattice
    """
    cuba_key = CUBA.BASE_CENTERED_ORTHORHOMBIC_LATTICE

    def __init__(self,
                 origin,
                 primitive_cell,
                 lattice_parameter=Default,
                 size=Default,
                 description=Default,
                 name=Default):
        super(BaseCenteredOrthorhombicLattice, self).__init__(
            lattice_parameter=lattice_parameter,
            origin=origin,
            primitive_cell=primitive_cell,
            size=size,
            description=description,
            name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(BaseCenteredOrthorhombicLattice,
                                cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([]) | base_params

    def _default_definition(self):
        return "A base centered orthorhombic lattice"  # noqa
