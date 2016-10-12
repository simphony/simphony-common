import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .thermostat import Thermostat
from . import validation


class Berendsen(Thermostat):
    '''The Berendsen thermostat model for temperature rescaling of all particles. The coupling time specifies how rapidly the temperature should be relaxed or coupled to the bath.  # noqa
    '''

    cuba_key = CUBA.BERENDSEN

    def __init__(self,
                 material,
                 description=None,
                 name=None,
                 data=None,
                 coupling_time=0.0001,
                 temperature=None):

        self.material = material
        self.description = description
        self.name = name
        if data:
            self.data = data
        self.coupling_time = coupling_time
        if temperature is None:
            self.temperature = [0.0, 0.0]
        # This is a system-managed, read-only attribute
        self._models = [CUBA.ATOMISTIC, CUBA.MESOSCOPIC]
        # This is a system-managed, read-only attribute
        self._definition = 'The Berendsen thermostat model for temperature rescaling of all particles. The coupling time specifies how rapidly the temperature should be relaxed or coupled to the bath.'  # noqa
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
    def coupling_time(self):
        return self.data[CUBA.COUPLING_TIME]

    @coupling_time.setter
    def coupling_time(self, value):
        value = validation.cast_data_type(value, 'coupling_time')
        validation.validate_cuba_keyword(value, 'coupling_time')
        self.data[CUBA.COUPLING_TIME] = value

    @property
    def temperature(self):
        return self.data[CUBA.TEMPERATURE]

    @temperature.setter
    def temperature(self, value):
        value = validation.cast_data_type(value, 'temperature')
        validation.check_shape(value, '(2)')
        for item in value:
            validation.validate_cuba_keyword(item, 'temperature')
        self.data[CUBA.TEMPERATURE] = value

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
        return (CUBA.TEMPERATURE, CUBA.COUPLING_TIME, CUBA.DESCRIPTION,
                CUBA.MATERIAL, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.THERMOSTAT, CUBA.MATERIAL_RELATION, CUBA.MODEL_EQUATION,
                CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
