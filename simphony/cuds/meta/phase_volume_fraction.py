from simphony.core import Default  # noqa
from simphony.cuds import meta_validation
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem


class PhaseVolumeFraction(CUDSItem):
    """
    volume fraction of a (one) phase (material) on a dataset
    entity
    """
    cuba_key = CUBA.PHASE_VOLUME_FRACTION

    def __init__(self, material, volume_fraction):
        super(PhaseVolumeFraction, self).__init__()
        self._init_volume_fraction(volume_fraction)
        self._init_material(material)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(PhaseVolumeFraction,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(
            set((
                CUBA.VOLUME_FRACTION,
                CUBA.MATERIAL, ) + base_params))

    def _default_definition(self):
        return "volume fraction of a (one) phase (material) on a dataset entity"  # noqa

    def _init_volume_fraction(self, value):
        if value is Default:
            value = self._default_volume_fraction()

        self.volume_fraction = value

    @property
    def volume_fraction(self):
        return self.data[CUBA.VOLUME_FRACTION]

    @volume_fraction.setter
    def volume_fraction(self, value):
        value = self._validate_volume_fraction(value)
        self.data[CUBA.VOLUME_FRACTION] = value

    def _validate_volume_fraction(self, value):
        value = meta_validation.cast_data_type(value, 'VOLUME_FRACTION')
        meta_validation.check_valid_shape(value, [1], 'VOLUME_FRACTION')
        meta_validation.validate_cuba_keyword(value, 'VOLUME_FRACTION')
        return value

    def _default_volume_fraction(self):
        raise TypeError("No default for volume_fraction")

    def _init_material(self, value):
        if value is Default:
            value = self._default_material()

        self.material = value

    @property
    def material(self):
        return self.data[CUBA.MATERIAL]

    @material.setter
    def material(self, value):
        value = self._validate_material(value)
        self.data[CUBA.MATERIAL] = value

    def _validate_material(self, value):
        value = meta_validation.cast_data_type(value, 'MATERIAL')
        meta_validation.check_valid_shape(value, [1], 'MATERIAL')
        meta_validation.validate_cuba_keyword(value, 'MATERIAL')
        return value

    def _default_material(self):
        raise TypeError("No default for material")
