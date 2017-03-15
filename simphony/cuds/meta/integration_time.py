from simphony.core import Default  # noqa
from simphony.cuds import meta_validation
from simphony.core.cuba import CUBA
from .solver_parameter import SolverParameter


class IntegrationTime(SolverParameter):
    """
    the current time, time step, and final time for a simulation
    stored on each cuds (a specific state).
    """
    cuba_key = CUBA.INTEGRATION_TIME

    def __init__(self,
                 current=Default,
                 final=Default,
                 size=Default,
                 description=Default,
                 name=Default):
        super(IntegrationTime, self).__init__(
            description=description, name=name)
        self._init_current(current)
        self._init_size(size)
        self._init_final(final)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(IntegrationTime, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(
            set((
                CUBA.CURRENT,
                CUBA.SIZE,
                CUBA.FINAL, ) + base_params))

    def _default_definition(self):
        return "the current time, time step, and final time for a simulation stored on each cuds (a specific state)."  # noqa

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
        value = meta_validation.cast_data_type(value, 'CURRENT')
        meta_validation.check_valid_shape(value, [1], 'CURRENT')
        meta_validation.validate_cuba_keyword(value, 'CURRENT')
        return value

    def _default_current(self):
        return 0.0

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
        value = meta_validation.cast_data_type(value, 'SIZE')
        meta_validation.check_valid_shape(value, [1], 'SIZE')
        meta_validation.validate_cuba_keyword(value, 'SIZE')
        return value

    def _default_size(self):
        return 0.0

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
        value = meta_validation.cast_data_type(value, 'FINAL')
        meta_validation.check_valid_shape(value, [1], 'FINAL')
        meta_validation.validate_cuba_keyword(value, 'FINAL')
        return value

    def _default_final(self):
        return 0.0
