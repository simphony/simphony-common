import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .rheology_model import RheologyModel
from . import validation


class HerschelBulkleyModel(RheologyModel):

    '''Herschel-Bulkley model combines the effects of Bingham plastic and power-law behavior in a fluid  # noqa
    '''

    cuba_key = CUBA.HERSCHEL_BULKLEY_MODEL

    def __init__(self, description=None, name=None, data=None, initial_viscosity=1e-3, relaxation_time=1.0, linear_constant=1e-5, power_law_index=1.0):

        self.description = description
        self.name = name
        if data:
            self.data = data
        self.initial_viscosity = initial_viscosity
        self.relaxation_time = relaxation_time
        self.linear_constant = linear_constant
        self.power_law_index = power_law_index
        # This is a system-managed, read-only attribute
        self._models = [CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'Herschel-Bulkley model combines the effects of Bingham plastic and power-law behavior in a fluid'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = []

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, DataContainer):
                raise TypeError("data is not a DataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, DataContainer):
            self._data = new_data
        else:
            self._data = DataContainer(new_data)

    @property
    def initial_viscosity(self):
        return self.data[CUBA.INITIAL_VISCOSITY]

    @initial_viscosity.setter
    def initial_viscosity(self, value):
        value = validation.cast_data_type(value, 'initial_viscosity')
        validation.validate_cuba_keyword(value, 'initial_viscosity')
        self.data[CUBA.INITIAL_VISCOSITY] = value

    @property
    def relaxation_time(self):
        return self.data[CUBA.RELAXATION_TIME]

    @relaxation_time.setter
    def relaxation_time(self, value):
        value = validation.cast_data_type(value, 'relaxation_time')
        validation.validate_cuba_keyword(value, 'relaxation_time')
        self.data[CUBA.RELAXATION_TIME] = value

    @property
    def linear_constant(self):
        return self.data[CUBA.LINEAR_CONSTANT]

    @linear_constant.setter
    def linear_constant(self, value):
        value = validation.cast_data_type(value, 'linear_constant')
        validation.validate_cuba_keyword(value, 'linear_constant')
        self.data[CUBA.LINEAR_CONSTANT] = value

    @property
    def power_law_index(self):
        return self.data[CUBA.POWER_LAW_INDEX]

    @power_law_index.setter
    def power_law_index(self, value):
        value = validation.cast_data_type(value, 'power_law_index')
        validation.validate_cuba_keyword(value, 'power_law_index')
        self.data[CUBA.POWER_LAW_INDEX] = value

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
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.DESCRIPTION, CUBA.INITIAL_VISCOSITY, CUBA.UUID, CUBA.POWER_LAW_INDEX, CUBA.RELAXATION_TIME, CUBA.LINEAR_CONSTANT, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.RHEOLOGY_MODEL, CUBA.PHYSICS_EQUATION, CUBA.MODEL_EQUATION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
