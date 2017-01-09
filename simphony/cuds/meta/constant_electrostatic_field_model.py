from simphony.core import Default  # noqa
from . import validation
from .electrostatic_model import ElectrostaticModel
from simphony.core.cuba import CUBA


class ConstantElectrostaticFieldModel(ElectrostaticModel):
    """
    A constant electrostatic field model
    """
    cuba_key = CUBA.CONSTANT_ELECTROSTATIC_FIELD_MODEL

    def __init__(self, electrostatic_field, description=Default, name=Default):

        super(ConstantElectrostaticFieldModel, self).__init__(
            description=description, name=name)
        self._init_electrostatic_field(electrostatic_field)

    def supported_parameters(self):
        try:
            base_params = super(ConstantElectrostaticFieldModel,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.ELECTROSTATIC_FIELD, ) + base_params

    def _default_models(self):
        return ['CUBA.MESOSCOPIC', 'CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "A constant electrostatic field model"  # noqa

    def _default_variables(self):
        return ['CUBA.ELECTRIC_FIELD', 'CUBA.CHARGE']  # noqa

    def _init_electrostatic_field(self, value):
        if value is Default:
            value = self._default_electrostatic_field()

        self.electrostatic_field = value

    @property
    def electrostatic_field(self):
        return self.data[CUBA.ELECTROSTATIC_FIELD]

    @electrostatic_field.setter
    def electrostatic_field(self, value):
        value = self._validate_electrostatic_field(value)
        self.data[CUBA.ELECTROSTATIC_FIELD] = value

    def _validate_electrostatic_field(self, value):
        value = validation.cast_data_type(value, 'ELECTROSTATIC_FIELD')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'ELECTROSTATIC_FIELD')
        return value

    def _default_electrostatic_field(self):
        return [0.0, 0.0, 0.0]
