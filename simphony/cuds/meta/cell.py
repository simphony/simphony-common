from simphony.core.cuba import CUBA
from .mesh_element import MeshElement


class Cell(MeshElement):
    """
    Element for storing 3D geometrical objects
    """

    cuba_key = CUBA.CELL

    def __init__(self, *args, **kwargs):
        super(Cell, self).__init__(*args, **kwargs)

        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(Cell, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_definition(self):
        self._definition = "Element for storing 3D geometrical objects"

    @property
    def definition(self):
        return self._definition
