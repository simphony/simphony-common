from simphony.core import Default  # noqa
from .neumann import Neumann
from simphony.core.cuba import CUBA
from simphony.cuds import meta_validation


class ZeroGradientVolumeFractionCondition(Neumann):
    """
    Zero gradient volume fraction condition
    """
    cuba_key = CUBA.ZERO_GRADIENT_VOLUME_FRACTION_CONDITION

    def __init__(self,
                 volume_fraction,
                 material,
                 description=Default,
                 name=Default):
        super(ZeroGradientVolumeFractionCondition, self).__init__(
            material=material, description=description, name=name)
        self._init_models()
        self._init_variables()
        self._init_volume_fraction(volume_fraction)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(ZeroGradientVolumeFractionCondition,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.VOLUME_FRACTION, ) + base_params))

    def _init_models(self):
        self._models = self._default_models()  # noqa

    @property
    def models(self):
        return self._models

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Zero gradient volume fraction condition"  # noqa

    def _init_variables(self):
        self._variables = self._default_variables()  # noqa

    @property
    def variables(self):
        return self._variables

    def _default_variables(self):
        return ['CUBA.VOLUME_FRACTION']  # noqa

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
