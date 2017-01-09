from .bravais_lattice import BravaisLattice
from simphony.core.cuba import CUBA


class BodyCenteredCubicLattice(BravaisLattice):
    """
    A body centred cubic lattice
    """
    cuba_key = CUBA.BODY_CENTERED_CUBIC_LATTICE

    def __init__(self,
                 primitive_cell,
                 origin,
                 lattice_parameter=Default,
                 size=Default,
                 description=Default,
                 name=Default):

        super(BodyCenteredCubicLattice, self).__init__(
            lattice_parameter=lattice_parameter,
            primitive_cell=primitive_cell,
            size=size,
            origin=origin,
            description=description,
            name=name)

    def supported_parameters(self):
        try:
            base_params = super(BodyCenteredCubicLattice,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "A body centred cubic lattice"  # noqa
