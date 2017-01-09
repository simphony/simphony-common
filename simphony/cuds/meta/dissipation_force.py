from .material_relation import MaterialRelation
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class DissipationForce(MaterialRelation):
    """
    Viscous normal force describing the inelasticity of particle
    collisions
    """
    cuba_key = CUBA.DISSIPATION_FORCE

    def __init__(self, restitution_coefficient=Default, *args, **kwargs):
        super(DissipationForce, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_restitution_coefficient(restitution_coefficient)

    def supported_parameters(self):
        try:
            base_params = super(DissipationForce, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.RESTITUTION_COEFFICIENT, ) + base_params

    def _init_models(self):
        self._models = ['CUBA.ATOMISTIC']  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Viscous normal force describing the inelasticity of particle collisions"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_restitution_coefficient(self, value):
        if value is Default:
            value = 1.0

        self.restitution_coefficient = value

    @property
    def restitution_coefficient(self):
        return self.data[CUBA.RESTITUTION_COEFFICIENT]

    @restitution_coefficient.setter
    def restitution_coefficient(self, value):
        value = self._validate_restitution_coefficient(value)
        self.data[CUBA.RESTITUTION_COEFFICIENT] = value

    def _validate_restitution_coefficient(self, value):
        value = validation.cast_data_type(value, 'RESTITUTION_COEFFICIENT')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'RESTITUTION_COEFFICIENT')
        return value
