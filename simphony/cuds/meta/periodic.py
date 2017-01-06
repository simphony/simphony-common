from .condition import Condition
from simphony.core.cuba import CUBA


class Periodic(Condition):
    """
    Periodic boundary condition (PBC)
    """

    cuba_key = CUBA.PERIODIC

    def __init__(self, *args, **kwargs):
        super(Periodic, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(Periodic, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = [
            'CUBA.ELECTRONIC', 'CUBA.ATOMISTIC', 'CUBA.MESOSCOPIC',
            'CUBA.CONTINUUM'
        ]

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Periodic boundary condition (PBC)"

    @property
    def definition(self):
        return self._definition
