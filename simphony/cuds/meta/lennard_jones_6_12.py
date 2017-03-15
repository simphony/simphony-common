from simphony.core import Default  # noqa
from simphony.cuds import meta_validation
from simphony.core.cuba import CUBA
from .pair_potential import PairPotential


class LennardJones_6_12(PairPotential):
    """
    A Lennard-Jones 6-12 Potential
    """
    cuba_key = CUBA.LENNARD_JONES_6_12

    def __init__(self,
                 material,
                 cutoff_distance=Default,
                 energy_well_depth=Default,
                 van_der_waals_radius=Default,
                 description=Default,
                 name=Default):
        super(LennardJones_6_12, self).__init__(
            material=material, description=description, name=name)
        self._init_van_der_waals_radius(van_der_waals_radius)
        self._init_cutoff_distance(cutoff_distance)
        self._init_energy_well_depth(energy_well_depth)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(LennardJones_6_12, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(
            set((
                CUBA.VAN_DER_WAALS_RADIUS,
                CUBA.CUTOFF_DISTANCE,
                CUBA.ENERGY_WELL_DEPTH, ) + base_params))

    def _default_definition(self):
        return "A Lennard-Jones 6-12 Potential"  # noqa

    def _init_van_der_waals_radius(self, value):
        if value is Default:
            value = self._default_van_der_waals_radius()

        self.van_der_waals_radius = value

    @property
    def van_der_waals_radius(self):
        return self.data[CUBA.VAN_DER_WAALS_RADIUS]

    @van_der_waals_radius.setter
    def van_der_waals_radius(self, value):
        value = self._validate_van_der_waals_radius(value)
        self.data[CUBA.VAN_DER_WAALS_RADIUS] = value

    def _validate_van_der_waals_radius(self, value):
        value = meta_validation.cast_data_type(value, 'VAN_DER_WAALS_RADIUS')
        meta_validation.check_valid_shape(value, [1], 'VAN_DER_WAALS_RADIUS')
        meta_validation.validate_cuba_keyword(value, 'VAN_DER_WAALS_RADIUS')
        return value

    def _default_van_der_waals_radius(self):
        return 1.0

    def _default_models(self):
        return ['CUBA.ATOMISTIC']  # noqa

    def _default_variables(self):
        return ['CUBA.POSITION', 'CUBA.POTENTIAL_ENERGY']  # noqa

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
        value = meta_validation.cast_data_type(value, 'CUTOFF_DISTANCE')
        meta_validation.check_valid_shape(value, [1], 'CUTOFF_DISTANCE')
        meta_validation.validate_cuba_keyword(value, 'CUTOFF_DISTANCE')
        return value

    def _default_cutoff_distance(self):
        return 1.0

    def _init_energy_well_depth(self, value):
        if value is Default:
            value = self._default_energy_well_depth()

        self.energy_well_depth = value

    @property
    def energy_well_depth(self):
        return self.data[CUBA.ENERGY_WELL_DEPTH]

    @energy_well_depth.setter
    def energy_well_depth(self, value):
        value = self._validate_energy_well_depth(value)
        self.data[CUBA.ENERGY_WELL_DEPTH] = value

    def _validate_energy_well_depth(self, value):
        value = meta_validation.cast_data_type(value, 'ENERGY_WELL_DEPTH')
        meta_validation.check_valid_shape(value, [1], 'ENERGY_WELL_DEPTH')
        meta_validation.validate_cuba_keyword(value, 'ENERGY_WELL_DEPTH')
        return value

    def _default_energy_well_depth(self):
        return 1.0
