from simphony.core import Default  # noqa
from .relative_velocity_model import RelativeVelocityModel
from simphony.core.cuba import CUBA
from simphony.cuds import meta_validation


class SimpleRelativeVelocityModel(RelativeVelocityModel):
    """
    Simple relative velocity model to use in mixture model
    """
    cuba_key = CUBA.SIMPLE_RELATIVE_VELOCITY_MODEL

    def __init__(self,
                 diffusion_velocity=Default,
                 linear_constant=Default,
                 description=Default,
                 name=Default):
        super(SimpleRelativeVelocityModel, self).__init__(
            description=description, name=name)
        self._init_linear_constant(linear_constant)
        self._init_diffusion_velocity(diffusion_velocity)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(SimpleRelativeVelocityModel,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(
            set((
                CUBA.LINEAR_CONSTANT,
                CUBA.DIFFUSION_VELOCITY, ) + base_params))

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Simple relative velocity model to use in mixture model"  # noqa

    def _init_linear_constant(self, value):
        if value is Default:
            value = self._default_linear_constant()

        self.linear_constant = value

    @property
    def linear_constant(self):
        return self.data[CUBA.LINEAR_CONSTANT]

    @linear_constant.setter
    def linear_constant(self, value):
        value = self._validate_linear_constant(value)
        self.data[CUBA.LINEAR_CONSTANT] = value

    def _validate_linear_constant(self, value):
        value = meta_validation.cast_data_type(value, 'LINEAR_CONSTANT')
        meta_validation.check_valid_shape(value, [1], 'LINEAR_CONSTANT')
        meta_validation.validate_cuba_keyword(value, 'LINEAR_CONSTANT')
        return value

    def _default_linear_constant(self):
        return 0.0

    def _init_diffusion_velocity(self, value):
        if value is Default:
            value = self._default_diffusion_velocity()

        self.diffusion_velocity = value

    @property
    def diffusion_velocity(self):
        return self.data[CUBA.DIFFUSION_VELOCITY]

    @diffusion_velocity.setter
    def diffusion_velocity(self, value):
        value = self._validate_diffusion_velocity(value)
        self.data[CUBA.DIFFUSION_VELOCITY] = value

    def _validate_diffusion_velocity(self, value):
        value = meta_validation.cast_data_type(value, 'DIFFUSION_VELOCITY')
        meta_validation.check_valid_shape(value, [1], 'DIFFUSION_VELOCITY')
        meta_validation.validate_cuba_keyword(value, 'DIFFUSION_VELOCITY')
        return value

    def _default_diffusion_velocity(self):
        return [0, 0, 0]
