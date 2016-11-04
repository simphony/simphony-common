import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .computational_method import ComputationalMethod


class Sph(ComputationalMethod):
    '''Smooth particle hydrodynamics  # noqa
    '''

    cuba_key = CUBA.SPH

    def __init__(self, description="", name=""):

        self._data = DataContainer()

        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._physics_equation = [CUBA.CFD]
        # This is a system-managed, read-only attribute
        self._definition = 'Smooth particle hydrodynamics'  # noqa

    @property
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    @property
    def physics_equation(self):
        return self._physics_equation

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
        return (CUBA.PHYSICS_EQUATION, CUBA.UUID, CUBA.DESCRIPTION, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.COMPUTATIONAL_METHOD, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
