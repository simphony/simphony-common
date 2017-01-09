from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA
from .pair_potential import PairPotential


class LennardJones_6_12(PairPotential):
    """
    A Lennard-Jones 6-12 Potential
    """
    cuba_key = CUBA.LENNARD_JONES_6_12

    def __init__(self,
                 van_der_waals_radius=Default,
                 cutoff_distance=Default,
                 energy_well_depth=Default,
                 *args,
                 **kwargs):
        super(LennardJones_6_12, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_van_der_waals_radius(van_der_waals_radius)
        self._init_models()
        self._init_variables()
        self._init_cutoff_distance(cutoff_distance)
        self._init_energy_well_depth(energy_well_depth)

    def supported_parameters(self):
        try:
            base_params = super(LennardJones_6_12, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.VAN_DER_WAALS_RADIUS,
            CUBA.CUTOFF_DISTANCE,
            CUBA.ENERGY_WELL_DEPTH, ) + base_params

    def _init_definition(self):
        self._definition = "A Lennard-Jones 6-12 Potential"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_van_der_waals_radius(self, value):
        if value is Default:
            value = 1.0

        self.van_der_waals_radius = value

    @property
    def van_der_waals_radius(self):
        return self.data[CUBA.VAN_DER_WAALS_RADIUS]

    @van_der_waals_radius.setter
    def van_der_waals_radius(self, value):
        value = self._validate_van_der_waals_radius(value)
        self.data[CUBA.VAN_DER_WAALS_RADIUS] = value

    def _validate_van_der_waals_radius(self, value):
        value = validation.cast_data_type(value, 'VAN_DER_WAALS_RADIUS')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'VAN_DER_WAALS_RADIUS')
        return value

    def _init_models(self):
        self._models = ['CUBA.ATOMISTIC']  # noqa

    @property
    def models(self):
        return self._models

    def _init_variables(self):
        self._variables = ['CUBA.POSITION', 'CUBA.POTENTIAL_ENERGY']  # noqa

    @property
    def variables(self):
        return self._variables

    def _init_cutoff_distance(self, value):
        if value is Default:
            value = 1.0

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

    def _init_energy_well_depth(self, value):
        if value is Default:
            value = 1.0

        self.energy_well_depth = value

    @property
    def energy_well_depth(self):
        return self.data[CUBA.ENERGY_WELL_DEPTH]

    @energy_well_depth.setter
    def energy_well_depth(self, value):
        value = self._validate_energy_well_depth(value)
        self.data[CUBA.ENERGY_WELL_DEPTH] = value

    def _validate_energy_well_depth(self, value):
        value = validation.cast_data_type(value, 'ENERGY_WELL_DEPTH')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'ENERGY_WELL_DEPTH')
        return value
