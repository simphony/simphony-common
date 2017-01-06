from . import validation
from simphony.core import Default
from .electrostatic_model import ElectrostaticModel
from simphony.core.cuba import CUBA


class ConstantElectrostaticFieldModel(ElectrostaticModel):
    """
    A constant electrostatic field model
    """
    cuba_key = CUBA.CONSTANT_ELECTROSTATIC_FIELD_MODEL

    def __init__(self, electrostatic_field=Default, *args, **kwargs):
        super(ConstantElectrostaticFieldModel, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_variables()
        self._init_electrostatic_field(electrostatic_field)

    def supported_parameters(self):
        try:
            base_params = super(ConstantElectrostaticFieldModel,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.ELECTROSTATIC_FIELD, ) + base_params

    def _init_models(self):
        self._models = ['CUBA.MESOSCOPIC', 'CUBA.CONTINUUM']  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "A constant electrostatic field model"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_variables(self):
        self._variables = ['CUBA.ELECTRIC_FIELD', 'CUBA.CHARGE']  # noqa

    @property
    def variables(self):
        return self._variables

    def _init_electrostatic_field(self, value):
        if value is Default:
            value = [0.0, 0.0, 0.0]

        self.electrostatic_field = value

    @property
    def electrostatic_field(self):
        return self.data[CUBA.ELECTROSTATIC_FIELD]

    @electrostatic_field.setter
    def electrostatic_field(self, value):
        value = self._validate_electrostatic_field(value)
        self.data[CUBA.ELECTROSTATIC_FIELD] = value

    def _validate_electrostatic_field(self, value):
        value = validation.cast_data_type(value, 'CUBA.ELECTROSTATIC_FIELD')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'CUBA.ELECTROSTATIC_FIELD')
        return value
