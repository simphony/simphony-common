from .solver_parameter import SolverParameter
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class IntegrationStep(SolverParameter):
    """
    the current step, integration step, and final number of
    steps for a simulation stored on each cuds (a specific
    state).
    """
    cuba_key = CUBA.INTEGRATION_STEP

    def __init__(self,
                 current=Default,
                 size=Default,
                 final=Default,
                 *args,
                 **kwargs):

        super(IntegrationStep, self).__init__(*args, **kwargs)
        self._init_current(current)
        self._init_size(size)
        self._init_final(final)

    def supported_parameters(self):
        try:
            base_params = super(IntegrationStep, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.CURRENT,
            CUBA.SIZE,
            CUBA.FINAL, ) + base_params

    def _default_definition(self):
        return "the current step, integration step, and final number of steps for a simulation stored on each cuds (a specific state)."  # noqa

    def _init_current(self, value):
        if value is Default:
            value = self._default_current()

        self.current = value

    @property
    def current(self):
        return self.data[CUBA.CURRENT]

    @current.setter
    def current(self, value):
        value = self._validate_current(value)
        self.data[CUBA.CURRENT] = value

    def _validate_current(self, value):
        value = validation.cast_data_type(value, 'CURRENT')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'CURRENT')
        return value

    def _default_current(self):
        return 0

    def _init_size(self, value):
        if value is Default:
            value = self._default_size()

        self.size = value

    @property
    def size(self):
        return self.data[CUBA.SIZE]

    @size.setter
    def size(self, value):
        value = self._validate_size(value)
        self.data[CUBA.SIZE] = value

    def _validate_size(self, value):
        value = validation.cast_data_type(value, 'SIZE')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'SIZE')
        return value

    def _default_size(self):
        return 0

    def _init_final(self, value):
        if value is Default:
            value = self._default_final()

        self.final = value

    @property
    def final(self):
        return self.data[CUBA.FINAL]

    @final.setter
    def final(self, value):
        value = self._validate_final(value)
        self.data[CUBA.FINAL] = value

    def _validate_final(self, value):
        value = validation.cast_data_type(value, 'FINAL')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'FINAL')
        return value

    def _default_final(self):
        return 0
