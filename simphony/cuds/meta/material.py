from simphony.core import Default  # noqa
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class Material(CUDSComponent):
    """
    Definition of a material and its properties in the data
    container
    """
    cuba_key = CUBA.MATERIAL

    def __init__(self, description=Default, name=Default):

        super(Material, self).__init__(description=description, name=name)

    def supported_parameters(self):
        try:
            base_params = super(Material, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Definition of a material and its properties in the data container"  # noqa
