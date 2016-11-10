import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .material_relation import MaterialRelation


class Thermostat(MaterialRelation):
    '''A thermostat is a model that describes the thermal interaction of a material with the environment or a heat reservoir  # noqa
    '''

    cuba_key = CUBA.THERMOSTAT

    def __init__(self, material, description="", name=""):

        self._data = DataContainer()

        self.material = material
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._models = [CUBA.ATOMISTIC, CUBA.MESOSCOPIC]
        # This is a system-managed, read-only attribute
        self._definition = 'A thermostat is a model that describes the thermal interaction of a material with the environment or a heat reservoir'  # noqa
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
        return DataContainer(self._data)

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
        return (CUBA.DESCRIPTION, CUBA.MATERIAL, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.MATERIAL_RELATION, CUBA.MODEL_EQUATION,
                CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
