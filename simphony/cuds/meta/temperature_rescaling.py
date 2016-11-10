import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .thermostat import Thermostat
from . import validation


class TemperatureRescaling(Thermostat):
    '''A simple temperature rescaling thermostat. The coupling time specifies how offen the temperature should be relaxed or coupled to the bath.  # noqa
    '''

    cuba_key = CUBA.TEMPERATURE_RESCALING

    def __init__(self,
                 material,
                 description="",
                 name="",
                 coupling_time=1e-06,
                 temperature=None):

        self._data = DataContainer()

        self.material = material
        if temperature is None:
            self.temperature = [0.0, 0.0]
        self.coupling_time = coupling_time
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._models = [CUBA.ATOMISTIC, CUBA.MESOSCOPIC]
        # This is a system-managed, read-only attribute
        self._definition = 'A simple temperature rescaling thermostat. The coupling time specifies how offen the temperature should be relaxed or coupled to the bath.'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = []

    @property
    def temperature(self):
        return self.data[CUBA.TEMPERATURE]

    @temperature.setter
    def temperature(self, value):
        value = validation.cast_data_type(value, 'temperature')
        validation.check_shape(value, '(2)')
        for item in value:
            validation.validate_cuba_keyword(item, 'temperature')
        data = self.data
        data[CUBA.TEMPERATURE] = value
        self.data = data

    @property
    def coupling_time(self):
        return self.data[CUBA.COUPLING_TIME]

    @coupling_time.setter
    def coupling_time(self, value):
        value = validation.cast_data_type(value, 'coupling_time')
        validation.validate_cuba_keyword(value, 'coupling_time')
        data = self.data
        data[CUBA.COUPLING_TIME] = value
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
        return (CUBA.COUPLING_TIME, CUBA.DESCRIPTION, CUBA.MATERIAL, CUBA.NAME,
                CUBA.TEMPERATURE, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.THERMOSTAT, CUBA.MATERIAL_RELATION, CUBA.MODEL_EQUATION,
                CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
