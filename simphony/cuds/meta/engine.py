from simphony.core import Default  # noqa
from . import validation
from simphony.core.cuba import CUBA
from .software_tool import SoftwareTool


class Engine(SoftwareTool):
    """
    Represents a software tool which is used to solve the
    physics equation
    """
    cuba_key = CUBA.ENGINE

    def __init__(self, engine_feature, version):

        super(Engine, self).__init__(version=version)
        self._init_engine_feature(engine_feature)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Engine, cls).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.ENGINE_FEATURE, ) + base_params

    def _default_definition(self):
        return "Represents a software tool which is used to solve the physics equation"  # noqa

    def _init_engine_feature(self, value):
        if value is Default:
            value = self._default_engine_feature()

        self.engine_feature = value

    @property
    def engine_feature(self):
        return self.data[CUBA.ENGINE_FEATURE]

    @engine_feature.setter
    def engine_feature(self, value):
        value = self._validate_engine_feature(value)
        self.data[CUBA.ENGINE_FEATURE] = value

    def _validate_engine_feature(self, value):
        value = validation.cast_data_type(value, 'ENGINE_FEATURE')
        validation.check_valid_shape(value, [None])
        validation.check_elements(value, [None], 'ENGINE_FEATURE')

        return value

    def _default_engine_feature(self):
        raise TypeError("No default for engine_feature")
