from .computational_model import ComputationalModel
from simphony.core.cuba import CUBA


class Atomistic(ComputationalModel):
    """
    Atomistic model category according to the RoMM
    """
    cuba_key = CUBA.ATOMISTIC

    def __init__(self, *args, **kwargs):

        super(Atomistic, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(Atomistic, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Atomistic model category according to the RoMM"  # noqa
