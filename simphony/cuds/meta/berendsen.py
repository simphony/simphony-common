from . import validation
from simphony.core import Default
from .thermostat import Thermostat
from simphony.core.cuba import CUBA


class Berendsen(Thermostat):
    """
    The Berendsen thermostat model for temperature rescaling of all particles. The coupling time specifies how rapidly the temperature should be relaxed or coupled to the bath.
    """

    cuba_key = CUBA.BERENDSEN

    def __init__(self,
                 coupling_time=Default,
                 temperature=Default,
                 *args,
                 **kwargs):
        super(Berendsen, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_coupling_time(coupling_time)
        self._init_temperature(temperature)

    def supported_parameters(self):
        try:
            base_params = super(Berendsen, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.COUPLING_TIME,
            CUBA.TEMPERATURE, ) + base_params

    def _init_models(self):
        self._models = ['CUBA.ATOMISTIC', 'CUBA.MESOSCOPIC']

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "The Berendsen thermostat model for temperature rescaling of all particles. The coupling time specifies how rapidly the temperature should be relaxed or coupled to the bath."

    @property
    def definition(self):
        return self._definition

    def _init_coupling_time(self, value):
        if value is Default:
            value = 0.0001

        self.coupling_time = value

    @property
    def coupling_time(self):
        return self.data[CUBA.COUPLING_TIME]

    @coupling_time.setter
    def coupling_time(self, value):
        value = self._validate_coupling_time(value)
        self.data[CUBA.COUPLING_TIME] = value

    def _validate_coupling_time(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.COUPLING_TIME')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.COUPLING_TIME')

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
        import itertools
        value = validation.cast_data_type(value, 'CUBA.TEMPERATURE')
        validation.check_shape(value, [2])
        for tuple_ in itertools.product(*[range(x) for x in [2]]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.TEMPERATURE')

        return value
