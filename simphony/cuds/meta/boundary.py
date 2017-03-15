from simphony.core import Default  # noqa
from .cuds_component import CUDSComponent
from simphony.core.cuba import CUBA
from simphony.cuds import meta_validation


class Boundary(CUDSComponent):
    """
    A computational boundary in the system, it includes
    translated physical boundaries to computational boundaries.
    """
    cuba_key = CUBA.BOUNDARY

    def __init__(self, condition=Default, description=Default, name=Default):
        super(Boundary, self).__init__(description=description, name=name)
        self._init_condition(condition)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Boundary, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.CONDITION, ) + base_params))

    def _default_definition(self):
        return "A computational boundary in the system, it includes translated physical boundaries to computational boundaries."  # noqa

    def _init_condition(self, value):
        if value is Default:
            value = self._default_condition()

        self.condition = value

    @property
    def condition(self):
        return self.data[CUBA.CONDITION]

    @condition.setter
    def condition(self, value):
        value = self._validate_condition(value)
        self.data[CUBA.CONDITION] = value

    def _validate_condition(self, value):
        value = meta_validation.cast_data_type(value, 'CONDITION')
        meta_validation.check_valid_shape(value, [None], 'CONDITION')
        meta_validation.check_elements(value, [None], 'CONDITION')

        return value

    def _default_condition(self):
        return []
