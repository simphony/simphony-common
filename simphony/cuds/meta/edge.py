from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .mesh_element import MeshElement


class Edge(MeshElement):
    """
    Element for storing 1D geometrical objects
    """
    cuba_key = CUBA.EDGE

    def __init__(self, point):

        super(Edge, self).__init__(point=point)

    def supported_parameters(self):
        try:
            base_params = super(Edge, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_definition(self):
        return "Element for storing 1D geometrical objects"  # noqa
