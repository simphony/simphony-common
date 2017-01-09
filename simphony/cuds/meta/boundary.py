from . import validation
from simphony.core import Default
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class Boundary(CUDSComponent):
    """
    A computational boundary in the system, it includes
    translated physical boundaries to computational boundaries.
    """
    cuba_key = CUBA.BOUNDARY

    def __init__(self, condition, *args, **kwargs):
        super(Boundary, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_condition(condition)

    def supported_parameters(self):
        try:
            base_params = super(Boundary, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.CONDITION, ) + base_params

    def _init_definition(self):
        self._definition = "A computational boundary in the system, it includes translated physical boundaries to computational boundaries."  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_condition(self, value):
        if value is Default:
            raise TypeError("Value for condition must be specified")

        self.condition = value

    @property
    def condition(self):
        return self.data[CUBA.CONDITION]

    @condition.setter
    def condition(self, value):
        value = self._validate_condition(value)
        self.data[CUBA.CONDITION] = value

    def _validate_condition(self, value):

        value = validation.cast_data_type(value, 'CONDITION')
        validation.check_shape(value, [None])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if has_attr(container, "flatten"):
            flat_array = container.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'CONDITION')

        return value
