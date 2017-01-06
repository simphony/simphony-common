from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class Material(CUDSComponent):
    """
    Definition of a material and its properties in the data container
    """

    cuba_key = CUBA.MATERIAL

    def __init__(self, *args, **kwargs):
        super(Material, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(Material, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "Definition of a material and its properties in the data container"

    @property
    def definition(self):
        return self._definition
