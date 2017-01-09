from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA
from .pair_potential import PairPotential


class Coulomb(PairPotential):
    """
    The standard electrostatic Coulombic interaction potential
    between a pair of point charges
    """
    cuba_key = CUBA.COULOMB

    def __init__(self,
                 cutoff_distance=Default,
                 dielectric_constant=Default,
                 *args,
                 **kwargs):

        super(Coulomb, self).__init__(*args, **kwargs)
        self._init_cutoff_distance(cutoff_distance)
        self._init_dielectric_constant(dielectric_constant)

    def supported_parameters(self):
        try:
            base_params = super(Coulomb, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.CUTOFF_DISTANCE,
            CUBA.DIELECTRIC_CONSTANT, ) + base_params

    def _default_models(self):
        return ['CUBA.ATOMISTIC']  # noqa

    def _default_definition(self):
        return "The standard electrostatic Coulombic interaction potential between a pair of point charges"  # noqa

    def _init_cutoff_distance(self, value):
        if value is Default:
            value = self._default_cutoff_distance()

        self.cutoff_distance = value

    @property
    def cutoff_distance(self):
        return self.data[CUBA.CUTOFF_DISTANCE]

    @cutoff_distance.setter
    def cutoff_distance(self, value):
        value = self._validate_cutoff_distance(value)
        self.data[CUBA.CUTOFF_DISTANCE] = value

    def _validate_cutoff_distance(self, value):
        value = validation.cast_data_type(value, 'CUTOFF_DISTANCE')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'CUTOFF_DISTANCE')
        return value

    def _default_cutoff_distance(self):
        return 1.0

    def _init_dielectric_constant(self, value):
        if value is Default:
            value = self._default_dielectric_constant()

        self.dielectric_constant = value

    @property
    def dielectric_constant(self):
        return self.data[CUBA.DIELECTRIC_CONSTANT]

    @dielectric_constant.setter
    def dielectric_constant(self, value):
        value = self._validate_dielectric_constant(value)
        self.data[CUBA.DIELECTRIC_CONSTANT] = value

    def _validate_dielectric_constant(self, value):
        value = validation.cast_data_type(value, 'DIELECTRIC_CONSTANT')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'DIELECTRIC_CONSTANT')
        return value

    def _default_dielectric_constant(self):
        return 1.0
