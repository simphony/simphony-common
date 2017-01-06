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

    def __init__(self, computational_method, physics_equation, *args,
                 **kwargs):
        super(EngineFeature, self).__init__(*args, **kwargs)

        self._init_computational_method(computational_method)
        self._init_definition()
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
            raise TypeError("Value for computational_method must be specified")

        self.computational_method = value

    @property
    def computational_method(self):
        return self.data[CUBA.COMPUTATIONAL_METHOD]

    @computational_method.setter
    def computational_method(self, value):
        value = self._validate_computational_method(value)
        self.data[CUBA.COMPUTATIONAL_METHOD] = value

    def _validate_computational_method(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.COMPUTATIONAL_METHOD')
        validation.check_shape(value, [None])
        for tuple_ in itertools.product(*[range(x) for x in [None]]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry,
                                             'CUBA.COMPUTATIONAL_METHOD')

        return value

    def _init_definition(self):
        self._definition = "Provides a physics equation and methods that engines provides to solve them"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_physics_equation(self, value):
        if value is Default:
            raise TypeError("Value for physics_equation must be specified")

        self.physics_equation = value

    @property
    def physics_equation(self):
        return self.data[CUBA.PHYSICS_EQUATION]

    @physics_equation.setter
    def physics_equation(self, value):
        value = self._validate_physics_equation(value)
        self.data[CUBA.PHYSICS_EQUATION] = value

    def _validate_physics_equation(self, value):
        value = validation.cast_data_type(value, 'CUBA.PHYSICS_EQUATION')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'CUBA.PHYSICS_EQUATION')
        return value
