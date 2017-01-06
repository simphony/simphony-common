from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class ComputationalModel(CUDSComponent):
    """
    Model category according to the RoMM
    """

    cuba_key = CUBA.COMPUTATIONAL_MODEL

    def __init__(self, *args, **kwargs):
        super(ComputationalModel, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(ComputationalModel,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "Model category according to the RoMM"

    @property
    def definition(self):
        return self._definition
