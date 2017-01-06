from .material_relation import MaterialRelation
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class SjkrCohesionForce(MaterialRelation):
    """
    Additional normal force tending to maintain the contact
    """

    cuba_key = CUBA.SJKR_COHESION_FORCE

    def __init__(self, cohesion_energy_density=Default, *args, **kwargs):
        super(SjkrCohesionForce, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_cohesion_energy_density(cohesion_energy_density)

    def supported_parameters(self):
        try:
            base_params = super(SjkrCohesionForce, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.COHESION_ENERGY_DENSITY, ) + base_params

    def _init_models(self):
        self._models = ['CUBA.ATOMISTIC']

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Additional normal force tending to maintain the contact"

    @property
    def definition(self):
        return self._definition

    def _init_cohesion_energy_density(self, value):
        if value is Default:
            value = 0.0

        self.cohesion_energy_density = value

    @property
    def cohesion_energy_density(self):
        return self.data[CUBA.COHESION_ENERGY_DENSITY]

    @cohesion_energy_density.setter
    def cohesion_energy_density(self, value):
        value = self._validate_cohesion_energy_density(value)
        self.data[CUBA.COHESION_ENERGY_DENSITY] = value

    def _validate_cohesion_energy_density(self, value):
        import itertools
        value = validation.cast_data_type(value,
                                          'CUBA.COHESION_ENERGY_DENSITY')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry,
                                             'CUBA.COHESION_ENERGY_DENSITY')

        return value
