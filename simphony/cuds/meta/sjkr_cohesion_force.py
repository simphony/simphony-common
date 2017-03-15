from simphony.core import Default  # noqa
from simphony.cuds import meta_validation
from simphony.core.cuba import CUBA
from .material_relation import MaterialRelation


class SjkrCohesionForce(MaterialRelation):
    """
    Additional normal force tending to maintain the contact
    """
    cuba_key = CUBA.SJKR_COHESION_FORCE

    def __init__(self,
                 cohesion_energy_density=Default,
                 material=Default,
                 description=Default,
                 name=Default):
        super(SjkrCohesionForce, self).__init__(
            material=material, description=description, name=name)
        self._init_cohesion_energy_density(cohesion_energy_density)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(SjkrCohesionForce, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.COHESION_ENERGY_DENSITY, ) + base_params))

    def _default_models(self):
        return ['CUBA.ATOMISTIC']  # noqa

    def _default_definition(self):
        return "Additional normal force tending to maintain the contact"  # noqa

    def _init_cohesion_energy_density(self, value):
        if value is Default:
            value = self._default_cohesion_energy_density()

        self.cohesion_energy_density = value

    @property
    def cohesion_energy_density(self):
        return self.data[CUBA.COHESION_ENERGY_DENSITY]

    @cohesion_energy_density.setter
    def cohesion_energy_density(self, value):
        value = self._validate_cohesion_energy_density(value)
        self.data[CUBA.COHESION_ENERGY_DENSITY] = value

    def _validate_cohesion_energy_density(self, value):
        value = meta_validation.cast_data_type(value,
                                               'COHESION_ENERGY_DENSITY')
        meta_validation.check_valid_shape(value, [1],
                                          'COHESION_ENERGY_DENSITY')
        meta_validation.validate_cuba_keyword(value, 'COHESION_ENERGY_DENSITY')
        return value

    def _default_cohesion_energy_density(self):
        return 0.0
