from simphony.core import Default
from . import validation
from .condition import Condition
from simphony.core.cuba import CUBA


class Empty(Condition):
    """
    Empty boundary condition
    """

    cuba_key = CUBA.EMPTY

    def __init__(self, variable=Default, material=Default, *args, **kwargs):
        super(Empty, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_variable(variable)
        self._init_material(material)

    def supported_parameters(self):
        try:
            base_params = super(Empty, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.VARIABLE,
            CUBA.MATERIAL, ) + base_params

    def _init_models(self):
        self._models = ['CUBA.CONTINUUM']

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Empty boundary condition"

    @property
    def definition(self):
        return self._definition

    def _init_variable(self, value):
        if value is Default:
            value = []

        self.variable = value

    @property
    def variable(self):
        return self.data[CUBA.VARIABLE]

    @variable.setter
    def variable(self, value):
        value = self._validate_variable(value)
        self.data[CUBA.VARIABLE] = value

    def _validate_variable(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.VARIABLE')
        validation.check_shape(value, [None])
        for tuple_ in itertools.product(*[range(x) for x in [None]]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.VARIABLE')

        return value

    def _init_material(self, value):
        if value is Default:
            value = []

        self.material = value

    @property
    def material(self):
        return self.data[CUBA.MATERIAL]

    @material.setter
    def material(self, value):
        value = self._validate_material(value)
        self.data[CUBA.MATERIAL] = value

    def _validate_material(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.MATERIAL')
        validation.check_shape(value, [None])
        for tuple_ in itertools.product(*[range(x) for x in [None]]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.MATERIAL')

        return value
