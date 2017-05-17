from simphony.core import Default  # noqa
from .condition import Condition
from simphony.core.cuba import CUBA


class FreeSlipVelocity(Condition):
    """
    Wall free slip velocity boundary condition, normal velocity
    is zero and tangential velocities are solved for.
    """
    cuba_key = CUBA.FREE_SLIP_VELOCITY

    def __init__(self, description=Default, name=Default):
        super(FreeSlipVelocity, self).__init__(
            description=description, name=name)
        self._init_variables()

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(FreeSlipVelocity, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_definition(self):
        return "Wall free slip velocity boundary condition, normal velocity is zero and tangential velocities are solved for."  # noqa

    def _init_variables(self):
        self._variables = self._default_variables()  # noqa

    @property
    def variables(self):
        return self._variables

    def _default_variables(self):
        return ['CUBA.VELOCITY']  # noqa
