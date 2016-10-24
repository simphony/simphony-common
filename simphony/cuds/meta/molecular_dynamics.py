import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation


class MolecularDynamics(PhysicsEquation):

    '''Classical atomistic molecular dynamics using Newtons equations of motion  # noqa
    '''

    cuba_key = CUBA.MOLECULAR_DYNAMICS

    def __init__(self, description=None, name=None, data=None):

        self.description = description
        self.name = name
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._models = [CUBA.ATOMISTIC]
        # This is a system-managed, read-only attribute
        self._definition = 'Classical atomistic molecular dynamics using Newtons equations of motion'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = [CUBA.POSITION, CUBA.VELOCITY, CUBA.MOMENTUM, CUBA.ACCELERATION, CUBA.FORCE]

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer()
            data_container = self._data

        # One more check in case the
        # property setter is by-passed
        if not isinstance(data_container, DataContainer):
            raise TypeError("data is not a DataContainer. "
                            "data.setter is by-passed.")
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
        return (CUBA.DESCRIPTION, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.PHYSICS_EQUATION, CUBA.MODEL_EQUATION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
