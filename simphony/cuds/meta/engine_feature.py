from .cuds_item import CUDSItem
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class EngineFeature(CUDSItem):
    """
    Provides a physics equation and methods that engines
    provides to solve them
    """
    cuba_key = CUBA.ENGINE_FEATURE

    def __init__(self, computational_method=Default, physics_equation=Default):

        super(EngineFeature, self).__init__()
        self._init_computational_method(computational_method)
        self._init_physics_equation(physics_equation)

    def supported_parameters(self):
        try:
            base_params = super(EngineFeature, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.COMPUTATIONAL_METHOD,
            CUBA.PHYSICS_EQUATION, ) + base_params

    def _init_computational_method(self, value):
        if value is Default:
            value = self._default_computational_method()

        self.computational_method = value

    @property
    def computational_method(self):
        return self.data[CUBA.COMPUTATIONAL_METHOD]

    @computational_method.setter
    def computational_method(self, value):
        value = self._validate_computational_method(value)
        self.data[CUBA.COMPUTATIONAL_METHOD] = value

    def _validate_computational_method(self, value):
        value = validation.cast_data_type(value, 'COMPUTATIONAL_METHOD')
        validation.check_shape(value, [None])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if hasattr(value, "flatten"):
            flat_array = value.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'COMPUTATIONAL_METHOD')

        return value

    def _default_computational_method(self):
        raise TypeError("No default for computational_method")

    def _default_definition(self):
        return "Provides a physics equation and methods that engines provides to solve them"  # noqa

    def _init_physics_equation(self, value):
        if value is Default:
            value = self._default_physics_equation()

        self.physics_equation = value

    @property
    def physics_equation(self):
        return self.data[CUBA.PHYSICS_EQUATION]

    @physics_equation.setter
    def physics_equation(self, value):
        value = self._validate_physics_equation(value)
        self.data[CUBA.PHYSICS_EQUATION] = value

    def _validate_physics_equation(self, value):
        value = validation.cast_data_type(value, 'PHYSICS_EQUATION')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'PHYSICS_EQUATION')
        return value

    def _default_physics_equation(self):
        raise TypeError("No default for physics_equation")
