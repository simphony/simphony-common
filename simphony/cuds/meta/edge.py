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

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Edge, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_definition(self):
        return "Element for storing 1D geometrical objects"  # noqa
