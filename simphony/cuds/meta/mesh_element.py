from .cuds_item import CUDSItem
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class MeshElement(CUDSItem):
    """
    An element for storing geometrical objects
    """
    cuba_key = CUBA.MESH_ELEMENT

    def __init__(self, point=Default):

        super(MeshElement, self).__init__()
        self._init_point(point)

    def supported_parameters(self):
        try:
            base_params = super(MeshElement, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.POINT, ) + base_params

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
        validation.check_shape(value, [None])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if hasattr(value, "flatten"):
            flat_array = value.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'POINT')

        return value

    def _default_point(self):
        raise TypeError("No default for point")
