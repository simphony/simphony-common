import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .multiphase_model import MultiphaseModel


class SinglePhaseModel(MultiphaseModel):
    '''A single phase fluid model  # noqa
    '''

    cuba_key = CUBA.SINGLE_PHASE_MODEL

    def __init__(self, description="", name=""):

        self._data = DataContainer()

        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._models = [CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'A single phase fluid model'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = []

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
        return (CUBA.MULTIPHASE_MODEL, CUBA.PHYSICS_EQUATION,
                CUBA.MODEL_EQUATION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
