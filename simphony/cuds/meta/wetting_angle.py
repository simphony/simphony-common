from simphony.core import Default  # noqa
from simphony.cuds import meta_validation
from simphony.core.cuba import CUBA
from .dirichlet import Dirichlet


class WettingAngle(Dirichlet):
    """
    Wetting angle Volume fraction wall boundary condition
    """
    cuba_key = CUBA.WETTING_ANGLE

    def __init__(self,
                 material,
                 contact_angle=Default,
                 description=Default,
                 name=Default):
        super(WettingAngle, self).__init__(
            material=material, description=description, name=name)
        self._init_models()
        self._init_contact_angle(contact_angle)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(WettingAngle, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((
            CUBA.MATERIAL,
            CUBA.CONTACT_ANGLE, ) + base_params))

    def _init_models(self):
        self._models = self._default_models()  # noqa

    @property
    def models(self):
        return self._models

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Wetting angle Volume fraction wall boundary condition"  # noqa

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
        meta_validation.check_valid_shape(value, [2], 'MATERIAL')
        meta_validation.check_elements(value, [2], 'MATERIAL')

        return value

    def _default_material(self):
        raise TypeError("No default for material")

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
        value = meta_validation.cast_data_type(value, 'CONTACT_ANGLE')
        meta_validation.check_valid_shape(value, [1], 'CONTACT_ANGLE')
        meta_validation.validate_cuba_keyword(value, 'CONTACT_ANGLE')
        return value

    def _default_contact_angle(self):
        return 90.0
