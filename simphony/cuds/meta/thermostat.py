from .material_relation import MaterialRelation
from simphony.core.cuba import CUBA


class Thermostat(MaterialRelation):
    """
    ['A thermostat is a model that describes the thermal', 'interaction of a material with the environment or a heat', 'reservoir']
    """

    cuba_key = CUBA.THERMOSTAT

    def __init__(self, *args, **kwargs):
        super(Thermostat, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(Thermostat, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = ['CUBA.ATOMISTIC', 'CUBA.MESOSCOPIC']  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "A thermostat is a model that describes the thermal interaction of a material with the environment or a heat reservoir"  # noqa

    @property
    def definition(self):
        return self._definition
