from simphony.core import Default  # noqa
from .condition import Condition
from simphony.core.cuba import CUBA


class InletOutlet(Condition):
    """
    Inlet outlet boundary condition (outlet condition is zero
    gradient and inlet given variable value)
    """
    cuba_key = CUBA.INLET_OUTLET

    def __init__(self, description=Default, name=Default):
        super(InletOutlet, self).__init__(description=description, name=name)
        self._init_models()

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(InletOutlet, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _init_models(self):
        self._models = self._default_models()  # noqa

    @property
    def models(self):
        return self._models

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Inlet outlet boundary condition (outlet condition is zero gradient and inlet given variable value)"  # noqa
