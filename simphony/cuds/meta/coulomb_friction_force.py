from simphony.core import Default  # noqa
from . import validation
from simphony.core.cuba import CUBA
from .material_relation import MaterialRelation


class CoulombFrictionForce(MaterialRelation):
    """
    Shear force accounting for the tangential displacement
    between contacting particles
    """
    cuba_key = CUBA.COULOMB_FRICTION_FORCE

    def __init__(self,
                 friction_coefficient=Default,
                 material=Default,
                 description=Default,
                 name=Default):
        super(CoulombFrictionForce, self).__init__(
            material=material, description=description, name=name)
        self._init_friction_coefficient(friction_coefficient)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(CoulombFrictionForce,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.FRICTION_COEFFICIENT, ) + base_params))

    def _default_models(self):
        return ['CUBA.ATOMISTIC']  # noqa

    def _default_definition(self):
        return "Shear force accounting for the tangential displacement between contacting particles"  # noqa

    def _init_friction_coefficient(self, value):
        if value is Default:
            value = self._default_friction_coefficient()

        self.friction_coefficient = value

    @property
    def friction_coefficient(self):
        return self.data[CUBA.FRICTION_COEFFICIENT]

    @friction_coefficient.setter
    def friction_coefficient(self, value):
        value = self._validate_friction_coefficient(value)
        self.data[CUBA.FRICTION_COEFFICIENT] = value

    def _validate_friction_coefficient(self, value):
        value = validation.cast_data_type(value, 'FRICTION_COEFFICIENT')
        validation.check_valid_shape(value, [1], 'FRICTION_COEFFICIENT')
        validation.validate_cuba_keyword(value, 'FRICTION_COEFFICIENT')
        return value

    def _default_friction_coefficient(self):
        return 0.0
