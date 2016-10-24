import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .turbulence_model import TurbulenceModel


class LaminarFlowModel(TurbulenceModel):
    '''Laminar model  # noqa
    '''

    cuba_key = CUBA.LAMINAR_FLOW_MODEL

    def __init__(self, description=None, name=None, data=None):

        self.description = description
        self.name = name
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._models = [CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'Laminar model'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = []

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer.new_with_restricted_keys(
                self.supported_parameters())
            data_container = self._data

        retvalue = DataContainer.new_with_restricted_keys(
            self.supported_parameters())
        retvalue.update(data_container)

        return retvalue

    @data.setter
    def data(self, new_data):
        data = DataContainer.new_with_restricted_keys(
            self.supported_parameters())
        data.update(new_data)
        self._data = data

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
        return (CUBA.TURBULENCE_MODEL, CUBA.PHYSICS_EQUATION,
                CUBA.MODEL_EQUATION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
