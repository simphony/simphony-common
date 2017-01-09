from . import validation
from simphony.core import Default
from .thermostat import Thermostat
from simphony.core.cuba import CUBA


class TemperatureRescaling(Thermostat):
    """
    A simple temperature rescaling thermostat. The coupling time
    specifies how offen the temperature should be relaxed or
    coupled to the bath.
    """
    cuba_key = CUBA.TEMPERATURE_RESCALING

    def __init__(self,
                 coupling_time=Default,
                 temperature=Default,
                 *args,
                 **kwargs):
        super(TemperatureRescaling, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_coupling_time(coupling_time)
        self._init_temperature(temperature)

    def supported_parameters(self):
        try:
            base_params = super(TemperatureRescaling,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.COUPLING_TIME,
            CUBA.TEMPERATURE, ) + base_params

    def _init_models(self):
        self._models = ['CUBA.ATOMISTIC', 'CUBA.MESOSCOPIC']  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "A simple temperature rescaling thermostat. The coupling time specifies how offen the temperature should be relaxed or coupled to the bath."  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_coupling_time(self, value):
        if value is Default:
            value = 1e-06

        self.coupling_time = value

    @property
    def coupling_time(self):
        return self.data[CUBA.COUPLING_TIME]

    @coupling_time.setter
    def coupling_time(self, value):
        value = self._validate_coupling_time(value)
        self.data[CUBA.COUPLING_TIME] = value

    def _validate_coupling_time(self, value):
        value = validation.cast_data_type(value, 'COUPLING_TIME')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'COUPLING_TIME')
        return value

    def _init_temperature(self, value):
        if value is Default:
            value = [0.0, 0.0]

        self.temperature = value

    @property
    def temperature(self):
        return self.data[CUBA.TEMPERATURE]

    @temperature.setter
    def temperature(self, value):
        value = self._validate_temperature(value)
        self.data[CUBA.TEMPERATURE] = value

    def _validate_temperature(self, value):

        value = validation.cast_data_type(value, 'TEMPERATURE')
        validation.check_shape(value, [2])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if has_attr(container, "flatten"):
            flat_array = container.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'TEMPERATURE')

        return value
