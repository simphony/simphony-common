from .software_tool import SoftwareTool
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class Engine(SoftwareTool):
    """
    Represents a software tool which is used to solve the
    physics equation
    """
    cuba_key = CUBA.ENGINE

    def __init__(self, engine_feature, *args, **kwargs):
        super(Engine, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_engine_feature(engine_feature)

    def supported_parameters(self):
        try:
            base_params = super(Engine, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.ENGINE_FEATURE, ) + base_params

    def _init_definition(self):
        self._definition = "Represents a software tool which is used to solve the physics equation"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_engine_feature(self, value):
        if value is Default:
            raise TypeError("Value for engine_feature must be specified")

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
        validation.check_shape(value, [None])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if has_attr(container, "flatten"):
            flat_array = container.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'ENGINE_FEATURE')

        return value
