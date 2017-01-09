from .cuds_item import CUDSItem
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class Point(CUDSItem):
    """
    A point in a 3D space system
    """
    cuba_key = CUBA.POINT

    def __init__(self, position=Default, *args, **kwargs):
        super(Point, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_position(position)

    def supported_parameters(self):
        try:
            base_params = super(Point, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.POSITION, ) + base_params

    def _init_definition(self):
        self._definition = "A point in a 3D space system"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_position(self, value):
        if value is Default:
            value = [0, 0, 0]

        self.position = value

    @property
    def position(self):
        return self.data[CUBA.POSITION]

    @position.setter
    def position(self, value):
        value = self._validate_position(value)
        self.data[CUBA.POSITION] = value

    def _validate_position(self, value):
        value = validation.cast_data_type(value, 'POSITION')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'POSITION')
        return value
