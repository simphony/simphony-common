from .computational_model import ComputationalModel
from simphony.core.cuba import CUBA


class Mesoscopic(ComputationalModel):
    """
    Mesoscopic model category according to the RoMM
    """
    cuba_key = CUBA.MESOSCOPIC

    def __init__(self, *args, **kwargs):
        super(Mesoscopic, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(Mesoscopic, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "Mesoscopic model category according to the RoMM"  # noqa

    @property
    def definition(self):
        return self._definition
