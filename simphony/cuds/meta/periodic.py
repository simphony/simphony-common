import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .condition import Condition


class Periodic(Condition):
    '''Periodic boundary condition (PBC)  # noqa
    '''

    cuba_key = CUBA.PERIODIC

    def __init__(self, description=None, name=None, data=None):

        self.description = description
        self.name = name
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._models = [
            CUBA.ELECTRONIC, CUBA.ATOMISTIC, CUBA.MESOSCOPIC, CUBA.CONTINUUM
        ]
        # This is a system-managed, read-only attribute
        self._definition = 'Periodic boundary condition (PBC)'  # noqa

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
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.DESCRIPTION, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CONDITION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
