from simphony.core import Default  # noqa
from . import validation
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class Node(CUDSComponent):
    """
    A node on a structured grid like lattice
    """
    cuba_key = CUBA.NODE

    def __init__(self, index, description=Default, name=Default):

        super(Node, self).__init__(description=description, name=name)
        self._init_index(index)

    def supported_parameters(self):
        try:
            base_params = super(Node, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.INDEX, ) + base_params

    def _default_definition(self):
        return "A node on a structured grid like lattice"  # noqa

    def _init_index(self, value):
        if value is Default:
            value = self._default_index()

        self.index = value

    @property
    def index(self):
        return self.data[CUBA.INDEX]

    @index.setter
    def index(self, value):
        value = self._validate_index(value)
        self.data[CUBA.INDEX] = value

    def _validate_index(self, value):
        value = validation.cast_data_type(value, 'INDEX')
        validation.check_shape_at_least(value, [1])
        validation.validate_cuba_keyword(value, 'INDEX')
        return value

    def _default_index(self):
        raise TypeError("No default for index")
