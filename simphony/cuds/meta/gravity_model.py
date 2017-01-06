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

    def _init_models(self):
        self._models = ['CUBA.MESOSCOPIC', 'CUBA.CONTINUUM']  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "A simple gravity model"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_variables(self):
        self._variables = ['CUBA.ACCELERATION']  # noqa

    @property
    def variables(self):
        return self._variables

    def _init_acceleration(self, value):
        if value is Default:
            value = [0.0, 0.0, 0.0]

        self.acceleration = value

    @property
    def acceleration(self):
        return self.data[CUBA.ACCELERATION]

    @acceleration.setter
    def acceleration(self, value):
        value = self._validate_acceleration(value)
        self.data[CUBA.ACCELERATION] = value

    def _validate_acceleration(self, value):
        value = validation.cast_data_type(value, 'CUBA.ACCELERATION')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'CUBA.ACCELERATION')
        return value
