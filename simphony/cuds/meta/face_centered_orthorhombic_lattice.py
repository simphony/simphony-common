from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class FaceCenteredOrthorhombicLattice(BravaisLattice):
    """
    A face centered orthorhombic lattice
    """
    cuba_key = CUBA.FACE_CENTERED_ORTHORHOMBIC_LATTICE

    def __init__(self,
                 primitive_cell,
                 origin,
                 lattice_parameter=Default,
                 size=Default,
                 description=Default,
                 name=Default):

        super(FaceCenteredOrthorhombicLattice, self).__init__(
            lattice_parameter=lattice_parameter,
            primitive_cell=primitive_cell,
            size=size,
            origin=origin,
            description=description,
            name=name)

    def supported_parameters(self):
        try:
            base_params = super(FaceCenteredOrthorhombicLattice,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A face centered orthorhombic lattice"  # noqa
