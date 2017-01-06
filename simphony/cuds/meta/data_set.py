from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA


class DataSet(CUDSComponent):
    """
    A representation of the computational entities of the model
    equations
    """
    cuba_key = CUBA.DATA_SET

    def __init__(self, *args, **kwargs):
        super(DataSet, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(DataSet, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = []  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "A representation of the computational entities of the model equations"  # noqa

    @property
    def definition(self):
        return self._definition
