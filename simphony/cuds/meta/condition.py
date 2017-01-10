from simphony.core import Default  # noqa
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class Condition(CUDSComponent):
    """
    Condition on boundaries or model entities
    """
    cuba_key = CUBA.CONDITION

    def __init__(self, description=Default, name=Default):

        super(Condition, self).__init__(description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Condition, cls).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Condition on boundaries or model entities"  # noqa
