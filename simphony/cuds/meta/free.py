from simphony.core import Default  # noqa
from .condition import Condition
from simphony.core.cuba import CUBA


class Free(Condition):
    """
    Free boundary condition
    """
    cuba_key = CUBA.FREE

    def __init__(self, description=Default, name=Default):

        super(Free, self).__init__(description=description, name=name)
        self._init_models()

    def supported_parameters(self):
        try:
            base_params = super(Free, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = self._default_models()  # noqa

    @property
    def models(self):
        return self._models

    def _default_models(self):
        return [
            'CUBA.ELECTRONIC', 'CUBA.ATOMISTIC', 'CUBA.MESOSCOPIC',
            'CUBA.CONTINUUM'
        ]  # noqa

    def _default_definition(self):
        return "Free boundary condition"  # noqa
