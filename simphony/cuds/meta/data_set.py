from simphony.core import Default  # noqa
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class DataSet(CUDSComponent):
    """
    A representation of the computational entities of the model
    equations
    """
    cuba_key = CUBA.DATA_SET

    def __init__(self, description=Default, name=Default):
        super(DataSet, self).__init__(description=description, name=name)
        self._init_models()

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(DataSet, cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([]) | base_params

    def _init_models(self):
        self._models = self._default_models()  # noqa

    @property
    def models(self):
        return self._models

    def _default_models(self):
        return []  # noqa

    def _default_definition(self):
        return "A representation of the computational entities of the model equations"  # noqa
