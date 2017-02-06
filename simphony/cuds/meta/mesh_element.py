from simphony.core import Default  # noqa
from . import validation
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem


class MeshElement(CUDSItem):
    """
    An element for storing geometrical objects
    """
    cuba_key = CUBA.MESH_ELEMENT

    def __init__(self, point):
        super(MeshElement, self).__init__()
        self._init_point(point)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(MeshElement, cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([CUBA.POINT, ]) | base_params

    def _default_definition(self):
        return "An element for storing geometrical objects"  # noqa

    def _init_point(self, value):
        if value is Default:
            value = self._default_point()

        self.point = value

    @property
    def point(self):
        return self.data[CUBA.POINT]

    @point.setter
    def point(self, value):
        value = self._validate_point(value)
        self.data[CUBA.POINT] = value

    def _validate_point(self, value):
        value = validation.cast_data_type(value, 'POINT')
        validation.check_valid_shape(value, [None], 'POINT')
        validation.check_elements(value, [None], 'POINT')

        return value

    def _default_point(self):
        raise TypeError("No default for point")
