from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .material_relation import MaterialRelation


class Thermostat(MaterialRelation):
    """
    A thermostat is a model that describes the thermal
    interaction of a material with the environment or a heat
    reservoir
    """
    cuba_key = CUBA.THERMOSTAT

    def __init__(self, material=Default, description=Default, name=Default):
        super(Thermostat, self).__init__(
            material=material, description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Thermostat, cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([]) | base_params

    def _default_models(self):
        return ['CUBA.ATOMISTIC', 'CUBA.MESOSCOPIC']  # noqa

    def _default_definition(self):
        return "A thermostat is a model that describes the thermal interaction of a material with the environment or a heat reservoir"  # noqa
