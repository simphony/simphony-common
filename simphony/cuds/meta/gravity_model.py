from .physics_equation import PhysicsEquation
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class GravityModel(PhysicsEquation):
    """
    A simple gravity model
    """
    cuba_key = CUBA.GRAVITY_MODEL

    def __init__(self, acceleration=Default, *args, **kwargs):

        super(GravityModel, self).__init__(*args, **kwargs)
        self._init_models()
        self._init_definition()
        self._init_variables()
        self._init_acceleration(acceleration)

    def supported_parameters(self):
        try:
            base_params = super(GravityModel, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.ACCELERATION, ) + base_params

    def _default_models(self):
        return ['CUBA.MESOSCOPIC', 'CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "A simple gravity model"  # noqa

    def _default_variables(self):
        return ['CUBA.ACCELERATION']  # noqa

    def _init_acceleration(self, value):
        if value is Default:
            value = self._default_acceleration()

        self.acceleration = value

    @property
    def acceleration(self):
        return self.data[CUBA.ACCELERATION]

    @acceleration.setter
    def acceleration(self, value):
        value = self._validate_acceleration(value)
        self.data[CUBA.ACCELERATION] = value

    def _validate_acceleration(self, value):
        value = validation.cast_data_type(value, 'ACCELERATION')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'ACCELERATION')
        return value

    def _default_acceleration(self):
        return [0.0, 0.0, 0.0]
