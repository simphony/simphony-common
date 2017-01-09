from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class Condition(CUDSComponent):
    """
    Condition on boundaries or model entities
    """
    cuba_key = CUBA.CONDITION

    def __init__(self, *args, **kwargs):

        super(Condition, self).__init__(*args, **kwargs)

    def supported_parameters(self):
        try:
            base_params = super(Condition, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Condition on boundaries or model entities"  # noqa
