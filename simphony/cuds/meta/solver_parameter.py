import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_component import CUDSComponent


class SolverParameter(CUDSComponent):
    '''Solver parameter and metadata  # noqa
    '''

    cuba_key = CUBA.SOLVER_PARAMETER

    def __init__(self, description="", name=""):

        self._data = DataContainer()

        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._definition = 'Solver parameter and metadata'  # noqa

    @property
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

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
        return (CUBA.UUID, CUBA.DESCRIPTION, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
