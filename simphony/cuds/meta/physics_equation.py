import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .model_equation import ModelEquation


class PhysicsEquation(ModelEquation):
    '''Physics equation  # noqa
    '''

    cuba_key = CUBA.PHYSICS_EQUATION

    def __init__(self, description="", name=""):

        self._data = DataContainer()

        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._definition = 'Physics equation'  # noqa
        # This is a system-managed, read-only attribute
        self._models = []
        # This is a system-managed, read-only attribute
        self._variables = []

    @property
    def definition(self):
        return self._definition

    @property
    def models(self):
        return self._models

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
        return (CUBA.DESCRIPTION, CUBA.NAME, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.MODEL_EQUATION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
