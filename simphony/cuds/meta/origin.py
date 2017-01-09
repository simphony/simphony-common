from . import validation
from simphony.core import Default
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class Origin(CUDSComponent):
    """
    The origin of a space system
    """
    cuba_key = CUBA.ORIGIN

    def __init__(self, position=Default, *args, **kwargs):

        super(Origin, self).__init__(*args, **kwargs)
        self._init_definition()
        self._init_position(position)

    def supported_parameters(self):
        try:
            base_params = super(Origin, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.POSITION, ) + base_params

    def _default_definition(self):
        return "The origin of a space system"  # noqa

    def _init_position(self, value):
        if value is Default:
            value = self._default_position()

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

    def _default_position(self):
        return [0, 0, 0]
