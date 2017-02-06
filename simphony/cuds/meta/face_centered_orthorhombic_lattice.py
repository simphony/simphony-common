from simphony.core import Default  # noqa
from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class FaceCenteredOrthorhombicLattice(BravaisLattice):
    """
    A face centered orthorhombic lattice
    """
    cuba_key = CUBA.FACE_CENTERED_ORTHORHOMBIC_LATTICE

    def __init__(self,
                 origin,
                 primitive_cell,
                 lattice_parameter=Default,
                 size=Default,
                 description=Default,
                 name=Default):
        super(FaceCenteredOrthorhombicLattice, self).__init__(
            lattice_parameter=lattice_parameter,
            origin=origin,
            primitive_cell=primitive_cell,
            size=size,
            description=description,
            name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(FaceCenteredOrthorhombicLattice,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_definition(self):
        return "A face centered orthorhombic lattice"  # noqa
