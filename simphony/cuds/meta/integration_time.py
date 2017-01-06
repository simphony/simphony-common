from .solver_parameter import SolverParameter
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class IntegrationTime(SolverParameter):
    """
    the current time, time step, and final time for a simulation stored on each cuds (a specific state).
    """

    cuba_key = CUBA.INTEGRATION_TIME

    def __init__(self,
                 current=Default,
                 size=Default,
                 final=Default,
                 *args,
                 **kwargs):
        super(IntegrationTime, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_current(current)
        self._init_size(size)
        self._init_final(final)

    def supported_parameters(self):
        try:
            base_params = super(IntegrationTime, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.CURRENT,
            CUBA.SIZE,
            CUBA.FINAL, ) + base_params

    def _init_definition(self):
        self._definition = "the current time, time step, and final time for a simulation stored on each cuds (a specific state)."

    @property
    def definition(self):
        return self._definition

    def _init_current(self, value):
        if value is Default:
            value = 0.0

        self.current = value

    @property
    def current(self):
        return self.data[CUBA.CURRENT]

    @current.setter
    def current(self, value):
        value = self._validate_current(value)
        self.data[CUBA.CURRENT] = value

    def _validate_current(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.CURRENT')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.CURRENT')

        return value

    def _init_size(self, value):
        if value is Default:
            value = 0.0

        self.size = value

    @property
    def size(self):
        return self.data[CUBA.SIZE]

    @size.setter
    def size(self, value):
        value = self._validate_size(value)
        self.data[CUBA.SIZE] = value

    def _validate_size(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.SIZE')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.SIZE')

        return value

    def _init_final(self, value):
        if value is Default:
            value = 0.0

        self.final = value

    @property
    def final(self):
        return self.data[CUBA.FINAL]

    @final.setter
    def final(self, value):
        value = self._validate_final(value)
        self.data[CUBA.FINAL] = value

    def _validate_final(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.FINAL')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.FINAL')

        return value
