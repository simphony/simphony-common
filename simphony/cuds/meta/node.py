from . import validation
from simphony.core import Default
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class Node(CUDSComponent):
    """
    A node on a structured grid like lattice
    """
    cuba_key = CUBA.NODE

    def __init__(self, index, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_index(index)

    def supported_parameters(self):
        try:
            base_params = super(Node, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.INDEX, ) + base_params

    def _init_definition(self):
        self._definition = "A node on a structured grid like lattice"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_index(self, value):
        if value is Default:
            raise TypeError("Value for index must be specified")

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
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'INDEX')
        return value
