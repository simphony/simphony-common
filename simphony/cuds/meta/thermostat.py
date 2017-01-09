from .material_relation import MaterialRelation
from simphony.core.cuba import CUBA


class Thermostat(MaterialRelation):
    """
    A thermostat is a model that describes the thermal
    interaction of a material with the environment or a heat
    reservoir
    """
    cuba_key = CUBA.THERMOSTAT

    def __init__(self, *args, **kwargs):

        super(Thermostat, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(Thermostat, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.ATOMISTIC', 'CUBA.MESOSCOPIC']  # noqa

    def _default_definition(self):
        return "A thermostat is a model that describes the thermal interaction of a material with the environment or a heat reservoir"  # noqa
