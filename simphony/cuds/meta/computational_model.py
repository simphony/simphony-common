from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class ComputationalModel(CUDSComponent):
    """
    Model category according to the RoMM
    """
    cuba_key = CUBA.COMPUTATIONAL_MODEL

    def __init__(self, *args, **kwargs):

        super(ComputationalModel, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(ComputationalModel,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Model category according to the RoMM"  # noqa
