import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .rheology_model import RheologyModel
from . import validation


class PowerLawViscosityModel(RheologyModel):
    '''Power law model for a variable viscosity function that is limited by minimum and maximum values  # noqa
    '''

    cuba_key = CUBA.POWER_LAW_VISCOSITY_MODEL

    def __init__(self,
                 description="",
                 name="",
                 linear_constant=1e-05,
                 minimum_viscosity=1e-05,
                 maximum_viscosity=0.001,
                 power_law_index=1.0):

        self._data = DataContainer()

        self.power_law_index = power_law_index
        self.maximum_viscosity = maximum_viscosity
        self.minimum_viscosity = minimum_viscosity
        self.linear_constant = linear_constant
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._models = [CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'Power law model for a variable viscosity function that is limited by minimum and maximum values'  # noqa
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
    def maximum_viscosity(self):
        return self.data[CUBA.MAXIMUM_VISCOSITY]

    @maximum_viscosity.setter
    def maximum_viscosity(self, value):
        value = validation.cast_data_type(value, 'maximum_viscosity')
        validation.validate_cuba_keyword(value, 'maximum_viscosity')
        data = self.data
        data[CUBA.MAXIMUM_VISCOSITY] = value
        self.data = data

    @property
    def minimum_viscosity(self):
        return self.data[CUBA.MINIMUM_VISCOSITY]

    @minimum_viscosity.setter
    def minimum_viscosity(self, value):
        value = validation.cast_data_type(value, 'minimum_viscosity')
        validation.validate_cuba_keyword(value, 'minimum_viscosity')
        data = self.data
        data[CUBA.MINIMUM_VISCOSITY] = value
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
        return DataContainer(self._data)

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
        return (CUBA.DESCRIPTION, CUBA.LINEAR_CONSTANT, CUBA.MAXIMUM_VISCOSITY,
                CUBA.MINIMUM_VISCOSITY, CUBA.NAME, CUBA.POWER_LAW_INDEX,
                CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.RHEOLOGY_MODEL, CUBA.PHYSICS_EQUATION,
                CUBA.MODEL_EQUATION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
