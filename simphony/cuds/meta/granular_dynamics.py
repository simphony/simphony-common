import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation


class GranularDynamics(PhysicsEquation):
    '''Granular dynamics of spherical particles using DEM  # noqa
    '''

    cuba_key = CUBA.GRANULAR_DYNAMICS

    def __init__(self, data=None, description="", name=""):

        self._data = DataContainer()

        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._models = [CUBA.MESOSCOPIC]
        # This is a system-managed, read-only attribute
        self._definition = 'Granular dynamics of spherical particles using DEM'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = [
            CUBA.POSITION, CUBA.VELOCITY, CUBA.MOMENTUM, CUBA.ACCELERATION,
            CUBA.MOMENT_INERTIA, CUBA.TORQUE, CUBA.ANGULAR_VELOCITY
        ]

    @property
    def data(self):
        return DataContainer(self._data)

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
        return (CUBA.PHYSICS_EQUATION, CUBA.MODEL_EQUATION,
                CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
