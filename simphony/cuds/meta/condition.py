from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class Condition(CUDSComponent):
    """
    ['Condition on boundaries or model entities']
    """

    cuba_key = CUBA.CONDITION

    def __init__(self, *args, **kwargs):
        super(Condition, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(Condition, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "Condition on boundaries or model entities"  # noqa

    @property
    def definition(self):
        return self._definition
