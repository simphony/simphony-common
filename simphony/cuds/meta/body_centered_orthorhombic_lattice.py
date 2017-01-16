from simphony.core import Default  # noqa
from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class BodyCenteredOrthorhombicLattice(BravaisLattice):
    """
    A body centered orthorhombic lattice
    """
    cuba_key = CUBA.BODY_CENTERED_ORTHORHOMBIC_LATTICE

    def __init__(self,
                 primitive_cell,
                 origin,
                 lattice_parameter=Default,
                 size=Default,
                 description=Default,
                 name=Default):

        super(BodyCenteredOrthorhombicLattice, self).__init__(
            lattice_parameter=lattice_parameter,
            primitive_cell=primitive_cell,
            size=size,
            origin=origin,
            description=description,
            name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(BodyCenteredOrthorhombicLattice,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A body centered orthorhombic lattice"  # noqa
