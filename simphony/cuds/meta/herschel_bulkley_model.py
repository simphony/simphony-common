import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .rheology_model import RheologyModel
from . import validation


class HerschelBulkleyModel(RheologyModel):
    '''Herschel-Bulkley model combines the effects of Bingham plastic and power-law behavior in a fluid  # noqa
    '''

    cuba_key = CUBA.HERSCHEL_BULKLEY_MODEL

    def __init__(self,
                 description="",
                 name="",
                 initial_viscosity=0.001,
                 relaxation_time=1.0,
                 linear_constant=1e-05,
                 power_law_index=1.0):

        self._data = DataContainer()

        self.power_law_index = power_law_index
        self.linear_constant = linear_constant
        self.relaxation_time = relaxation_time
        self.initial_viscosity = initial_viscosity
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._models = [CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'Herschel-Bulkley model combines the effects of Bingham plastic and power-law behavior in a fluid'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = []

    @property
    def power_law_index(self):
        return self.data[CUBA.POWER_LAW_INDEX]

    @power_law_index.setter
    def power_law_index(self, value):
        value = validation.cast_data_type(value, 'power_law_index')
        validation.validate_cuba_keyword(value, 'power_law_index')
        data = self.data
        data[CUBA.POWER_LAW_INDEX] = value
        self.data = data

    @property
    def linear_constant(self):
        return self.data[CUBA.LINEAR_CONSTANT]

    @linear_constant.setter
    def linear_constant(self, value):
        value = validation.cast_data_type(value, 'linear_constant')
        validation.validate_cuba_keyword(value, 'linear_constant')
        data = self.data
        data[CUBA.LINEAR_CONSTANT] = value
        self.data = data

    @property
    def relaxation_time(self):
        return self.data[CUBA.RELAXATION_TIME]

    @relaxation_time.setter
    def relaxation_time(self, value):
        value = validation.cast_data_type(value, 'relaxation_time')
        validation.validate_cuba_keyword(value, 'relaxation_time')
        data = self.data
        data[CUBA.RELAXATION_TIME] = value
        self.data = data

    @property
    def initial_viscosity(self):
        return self.data[CUBA.INITIAL_VISCOSITY]

    @initial_viscosity.setter
    def initial_viscosity(self, value):
        value = validation.cast_data_type(value, 'initial_viscosity')
        validation.validate_cuba_keyword(value, 'initial_viscosity')
        data = self.data
        data[CUBA.INITIAL_VISCOSITY] = value
        self.data = data

    @property
    def models(self):
        return self._models

    @property
    def definition(self):
        return self._definition

    @property
    def variables(self):
        return self._variables

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.DESCRIPTION, CUBA.INITIAL_VISCOSITY, CUBA.LINEAR_CONSTANT,
                CUBA.NAME, CUBA.POWER_LAW_INDEX, CUBA.RELAXATION_TIME,
                CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.RHEOLOGY_MODEL, CUBA.PHYSICS_EQUATION,
                CUBA.MODEL_EQUATION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
