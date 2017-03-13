from simphony.core import Default  # noqa
from . import validation
from .condition import Condition
from simphony.core.cuba import CUBA


class WettingAngle(Condition):
    """
    Volume fraction wall boundary condition with specified
    contact angle
    """
    cuba_key = CUBA.WETTING_ANGLE

    def __init__(self,
                 contact_angle=Default,
                 variable=Default,
                 description=Default,
                 name=Default):
        super(WettingAngle, self).__init__(description=description, name=name)
        self._init_models()
        self._init_variable(variable)
        self._init_contact_angle(contact_angle)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(WettingAngle, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.VARIABLE, CUBA.CONTACT_ANGLE, ) + base_params))

    def _init_models(self):
        self._models = self._default_models()  # noqa

    @property
    def models(self):
        return self._models

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Volume fraction wall boundary condition with specified contact angle"  # noqa

    def _init_variable(self, value):
        if value is Default:
            value = self._default_variable()

        self.variable = value

    @property
    def variable(self):
        return self.data[CUBA.VARIABLE]

    @variable.setter
    def variable(self, value):
        value = self._validate_variable(value)
        self.data[CUBA.VARIABLE] = value

    def _validate_variable(self, value):
        value = validation.cast_data_type(value, 'VARIABLE')
        validation.check_valid_shape(value, [None], 'VARIABLE')
        validation.check_elements(value, [None], 'VARIABLE')

        return value

    def _default_variable(self):
        return []

    def _init_contact_angle(self, value):
        if value is Default:
            value = self._default_contact_angle()

        self.contact_angle = value

    @property
    def contact_angle(self):
        return self.data[CUBA.CONTACT_ANGLE]

    @contact_angle.setter
    def contact_angle(self, value):
        value = self._validate_contact_angle(value)
        self.data[CUBA.CONTACT_ANGLE] = value

    def _validate_contact_angle(self, value):
        value = validation.cast_data_type(value, 'CONTACT_ANGLE')
        validation.check_valid_shape(value, [1], 'CONTACT_ANGLE')
        validation.validate_cuba_keyword(value, 'CONTACT_ANGLE')
        return value

    def _default_contact_angle(self):
        return 45.0
