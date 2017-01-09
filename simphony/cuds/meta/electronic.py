from .computational_model import ComputationalModel
from simphony.core.cuba import CUBA


class Electronic(ComputationalModel):
    """
    Electronic model category according to the RoMM
    """
    cuba_key = CUBA.ELECTRONIC

    def __init__(self, *args, **kwargs):

        super(Electronic, self).__init__(*args, **kwargs)
        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(Electronic, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Electronic model category according to the RoMM"  # noqa
