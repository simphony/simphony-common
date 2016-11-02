import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation
from . import validation


class GravityModel(PhysicsEquation):
    '''A simple gravity model  # noqa
    '''

    cuba_key = CUBA.GRAVITY_MODEL

    def __init__(self,
                 acceleration=None,
                 description=None,
                 name=None,
                 data=None):

        if acceleration is None:
            self.acceleration = [0.0, 0.0, 0.0]
        self.description = description
        self.name = name
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._models = [CUBA.MESOSCOPIC, CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'A simple gravity model'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = [CUBA.ACCELERATION]

    @property
    def acceleration(self):
        return self.data[CUBA.ACCELERATION]

    @acceleration.setter
    def acceleration(self, value):
        value = validation.cast_data_type(value, 'acceleration')
        validation.validate_cuba_keyword(value, 'acceleration')
        data = self.data
        data[CUBA.ACCELERATION] = value
        self.data = data

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer()
            data_container = self._data

        return DataContainer(data_container)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

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
        return (CUBA.ACCELERATION, CUBA.DESCRIPTION, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.PHYSICS_EQUATION, CUBA.MODEL_EQUATION,
                CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
