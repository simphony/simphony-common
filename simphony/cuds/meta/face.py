from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .mesh_element import MeshElement


class Face(MeshElement):
    """
    Element for storing 2D geometrical objects
    """
    cuba_key = CUBA.FACE

    def __init__(self, point):

        super(Face, self).__init__(point=point)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Face, cls).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Element for storing 2D geometrical objects"  # noqa
