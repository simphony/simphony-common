from . import validation
from simphony.core import Default
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class Boundary(CUDSComponent):
    """
    A computational boundary in the system, it includes translated physical boundaries to computational boundaries.
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
        self._definition = "A computational boundary in the system, it includes translated physical boundaries to computational boundaries."

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
        import itertools
        value = validation.cast_data_type(value, 'CUBA.CONDITION')
        validation.check_shape(value, [None])
        for tuple_ in itertools.product(*[range(x) for x in [None]]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.CONDITION')

        return value
