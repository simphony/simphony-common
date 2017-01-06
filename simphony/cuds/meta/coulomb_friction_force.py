from .material_relation import MaterialRelation
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class CoulombFrictionForce(MaterialRelation):
    """
    Shear force accounting for the tangential displacement between contacting particles
    """

    cuba_key = CUBA.COULOMB_FRICTION_FORCE

    def __init__(self, friction_coefficient=Default, *args, **kwargs):
        super(CoulombFrictionForce, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_friction_coefficient(friction_coefficient)

    def supported_parameters(self):
        try:
            base_params = super(CoulombFrictionForce,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.FRICTION_COEFFICIENT, ) + base_params

    def _init_models(self):
        self._models = ['CUBA.ATOMISTIC']

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Shear force accounting for the tangential displacement between contacting particles"

    @property
    def definition(self):
        return self._definition

    def _init_friction_coefficient(self, value):
        if value is Default:
            value = 0.0

        self.friction_coefficient = value

    @property
    def friction_coefficient(self):
        return self.data[CUBA.FRICTION_COEFFICIENT]

    @friction_coefficient.setter
    def friction_coefficient(self, value):
        value = self._validate_friction_coefficient(value)
        self.data[CUBA.FRICTION_COEFFICIENT] = value

    def _validate_friction_coefficient(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.FRICTION_COEFFICIENT')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry,
                                             'CUBA.FRICTION_COEFFICIENT')

        return value
