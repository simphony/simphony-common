from simphony.core import Default  # noqa
from simphony.cuds import meta_validation
from simphony.core.cuba import CUBA
from .phase_volume_fraction import PhaseVolumeFraction


class PhaseVolumeFractions(PhaseVolumeFraction):
    """
    volume fractions for a number of phases (material) on a
    dataset entity
    """
    cuba_key = CUBA.PHASE_VOLUME_FRACTIONS

    def __init__(self, phase_volume_fraction, material, volume_fraction):
        super(PhaseVolumeFractions, self).__init__(
            material=material, volume_fraction=volume_fraction)
        self._init_phase_volume_fraction(phase_volume_fraction)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(PhaseVolumeFractions,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.PHASE_VOLUME_FRACTION, ) + base_params))

    def _default_definition(self):
        return "volume fractions for a number of phases (material) on a dataset entity"  # noqa

    def _init_phase_volume_fraction(self, value):
        if value is Default:
            value = self._default_phase_volume_fraction()

        self.phase_volume_fraction = value

    @property
    def phase_volume_fraction(self):
        return self.data[CUBA.PHASE_VOLUME_FRACTION]

    @phase_volume_fraction.setter
    def phase_volume_fraction(self, value):
        value = self._validate_phase_volume_fraction(value)
        self.data[CUBA.PHASE_VOLUME_FRACTION] = value

    def _validate_phase_volume_fraction(self, value):
        value = meta_validation.cast_data_type(value, 'PHASE_VOLUME_FRACTION')
        meta_validation.check_valid_shape(value, [None],
                                          'PHASE_VOLUME_FRACTION')
        meta_validation.check_elements(value, [None], 'PHASE_VOLUME_FRACTION')

        return value

    def _default_phase_volume_fraction(self):
        raise TypeError("No default for phase_volume_fraction")
