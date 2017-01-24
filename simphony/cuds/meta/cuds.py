from simphony.core import Default  # noqa
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class CUDS(CUDSComponent):
    """
    CUDS Container
    """
    cuba_key = CUBA.CUDS

    def __init__(self, description=Default, name=Default):

        super(CUDS, self).__init__(description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(CUDS, cls).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "CUDS Container"  # noqa
